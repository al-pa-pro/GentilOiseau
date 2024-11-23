
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from services.extensions import db
from services.models import Utilisateur, Liste, ListeOiseau, Oiseau, Chant




liste_routes = Blueprint('liste_routes', __name__)



@liste_routes.route('/oiseaux')
def oiseaux():
    oiseaux = db.session.query(Oiseau).join(Chant).distinct(Oiseau.nom_scientifique)
    return render_template('oiseaux.html', oiseaux=oiseaux)

# Afficher les listes d'un utilisateur
@liste_routes.route('/mes_listes')
def mes_listes():
    listes = Liste.query.filter_by(utilisateur_id=session['user_id']).all()
    return render_template('mes_listes.html', listes=listes)

# Créer une nouvelle liste
@liste_routes.route('/creer_liste', methods=['GET', 'POST'])
def creer_liste():
    if request.method == 'POST':
        nom = request.form['nom']
        nouvelle_liste = Liste(nom=nom, utilisateur_id=session['user_id'])
        db.session.add(nouvelle_liste)
        db.session.commit()
        flash("Liste créée avec succès.")
        return redirect(url_for('mes_listes'))
    return render_template('mes_listes.html')

# Ajouter un oiseau à une liste existante
@liste_routes.route('/ajouter_aa_liste/<liste_id>/<oiseau_id>', methods=['POST'])
def ajouter_aa_liste(liste_id, oiseau_id):
    liste_oiseau = ListeOiseau(liste_id=liste_id, oiseau_id=oiseau_id)
    db.session.add(liste_oiseau)
    db.session.commit()
    flash("Oiseau ajouté à la liste.")
    return redirect(url_for('oiseaux'))

@liste_routes.route('/ajouter_a_liste', methods=['POST'])
def ajouter_a_liste():
    liste_id = request.form.get('liste_id')
    oiseaux_ids = request.form.getlist('oiseaux')

    liste = db.session.query(Liste).filter_by(id=liste_id).first()
    if not liste:
        return jsonify({"error": "Liste non trouvée"}), 404

    # Ajouter les oiseaux à la liste
    for oiseau_id in oiseaux_ids:
        oiseau = db.session.query(Oiseau).filter_by(id_oiseau=oiseau_id).first()
        if oiseau:
            liste.oiseaux.append(oiseau)

    db.session.commit()
    return jsonify({"message": "Oiseaux ajoutés avec succès"}), 200