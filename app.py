import os
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory
from itsdangerous import URLSafeTimedSerializer

from services.extensions import db, mail, login_manager
from services.models import Utilisateur
from routes.auth_routes import auth_routes
from routes.quiz_routes import quiz_routes
from routes.liste_routes import liste_routes

# Charger les variables d'environnement
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    # Configurations principales
    app.config['UPLOAD_FOLDER'] = 'static/uploads/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'BDDsqlite', 'oiseaux.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'mp3'}

    # Initialiser les extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth_routes.login"

    @login_manager.user_loader
    def load_user(user_id):
        return Utilisateur.query.get(int(user_id))
    

    # Enregistrer les blueprints
    app.register_blueprint(auth_routes)
    app.register_blueprint(quiz_routes)
    app.register_blueprint(liste_routes)

    #route de base pour l'accueil
    @app.route('/')
    def accueil():
        return render_template('accueil.html')
    
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/uploads/<region>/<filename>')
    def serve_audio(region, filename):
        # Vérifier si la région existe dans le dossier uploads
        region_folder = os.path.join(app.config['UPLOAD_FOLDER'], region)
        
        if not os.path.exists(region_folder):
            return "Région introuvable", 404  # Si la région n'existe pas, retour d'une erreur 404
        
        # Retourner le fichier audio depuis le sous-dossier de la région
        return send_from_directory(region_folder, filename)

    return app




# Créer l'application
app = create_app()



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
