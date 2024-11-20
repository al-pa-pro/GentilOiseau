from services.extensions import db


class Utilisateur(db.Model):
    id_utilisateur = db.Column(db.Integer, primary_key=True)
    nom_utilisateur = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(128), nullable=False)
    reset_token = db.Column(db.String(120), nullable=True)

        # Méthodes nécessaires pour Flask-Login
    def is_active(self):
        return True  # L'utilisateur est toujours actif

    def get_id(self):
        return str(self.id_utilisateur)  # Cette méthode est nécessaire pour Flask-Login

    def is_authenticated(self):
        return True  # L'utilisateur est authentifié si nous n'avons pas de logique supplémentaire

    def is_anonymous(self):
        return False  # L'utilisateur n'est pas anonyme
    

    def __repr__(self):
        return f"<Utilisateur(id_utilisateur={self.id_utilisateur}, nom_utilisateur={self.nom_utilisateur}, email={self.email})>"