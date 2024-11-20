import os
from dotenv import load_dotenv
from flask import Flask, render_template
from itsdangerous import URLSafeTimedSerializer

from services.extensions import db, mail, login_manager
from services.models import Utilisateur
from routes.auth_routes import auth_routes

# Charger les variables d'environnement
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY



    # Configurations principales
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

    #route de base pour l'accueil
    @app.route('/')
    def accueil():
        return render_template('accueil.html')

    return app



# Créer l'application
app = create_app()



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
