import os

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from services.extensions import db, mail
from services.models import Utilisateur
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement depuis le fichier .env
SECRET_KEY = os.getenv("SECRET_KEY")
MAIL_USERNAME=os.getenv("MAIL_USERNAME")

serializer = URLSafeTimedSerializer(SECRET_KEY)


auth_routes = Blueprint('auth_routes', __name__)

# Inscription
@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        nom_utilisateur = request.form['nom_utilisateur']
        mot_de_passe = request.form['mot_de_passe']
        mot_de_passe_hache = generate_password_hash(mot_de_passe)

        # Vérifiez si l'email existe déjà dans la base de données
        utilisateur_existant = Utilisateur.query.filter_by(email=email).first()
        if utilisateur_existant:
            flash("Cet email est déjà utilisé. Veuillez en choisir un autre.")
            return redirect(url_for('auth_routes.register'))

        nouvel_utilisateur = Utilisateur(email=email, nom_utilisateur=nom_utilisateur, mot_de_passe=mot_de_passe_hache)
        db.session.add(nouvel_utilisateur)
        db.session.commit()
        
        flash("Inscription réussie ! Vous pouvez maintenant vous connecter.")
        return redirect(url_for('auth_routes.login'))
    return render_template('register.html')

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        utilisateur = Utilisateur.query.filter_by(email=email).first()

        if utilisateur and check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
            # Enregistrer l'utilisateur dans la session
            session['id_utilisateur'] = utilisateur.id_utilisateur
            session['nom_utilisateur'] = utilisateur.nom_utilisateur
            session['email_utilisateur'] = utilisateur.email

            # Connexion via Flask-Login
            login_user(utilisateur)
            
            flash("Connexion réussie !")
            return redirect(url_for('accueil'))
        
        # Gérer les erreurs
        if not utilisateur:
            flash("Email non trouvé.")
        else:
            flash("Mot de passe incorrect.")

    return render_template('login.html')




# Réinitialisation de mot de passe
@auth_routes.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        utilisateur = Utilisateur.query.filter_by(email=email).first()
        if utilisateur:
            token = serializer.dumps(email, salt='password-reset-salt')
            utilisateur.reset_token = token 
            db.session.commit()
            # Cree un lien de reinitialisation
            reset_url = url_for('auth_routes.reset_password', token=token, _external=True)

            # Ici, envoyer un email contenant le lien de réinitialisation avec le token
            
            msg = Message('Requete de reinitialisation de mot de passe', recipients=[email], sender=MAIL_USERNAME)
            msg.body = f"Pour réinitialiser votre mot de passe: {reset_url} Si ce n'est pas votre requête, veuillez ignorer."
            msg.charset = 'utf-8' 
            mail.send(msg)
                    
            flash("Un lien de réinitialisation a été envoyé.")
            return redirect(url_for('auth_routes.login'))
        
        else:
            flash("Aucun compte trouvé avec cet email.")
    return render_template('forgot_password.html')

@auth_routes.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Charge l'email à partir du token
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # Le token expire après 1 heure
        print(email)
        utilisateur = Utilisateur.query.filter_by(email=email).first()
    except:
        flash('The reset link is invalid or has expired.', 'warning')
        return redirect(url_for('auth_routes.forgot_password'))
    
    print(token)
    print(utilisateur.reset_token)

    if request.method == 'POST' and token==utilisateur.reset_token:
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            hashed_new_password = generate_password_hash(
            new_password, method='pbkdf2:sha256')
            utilisateur = Utilisateur.query.filter_by(email=email).first()
            hashed_new_password = generate_password_hash(new_password, method='pbkdf2:sha256')
            utilisateur.mot_de_passe = hashed_new_password
            utilisateur.reset_token=None
            db.session.commit()
            
        return redirect(url_for('auth_routes.login'))
    return render_template("reset_password.html")


@auth_routes.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Vous avez ete deconnecte', 'info')  # Ajoutez un message flash
    # Redirigez vers la page d'accueil
    return redirect(url_for('accueil'))
