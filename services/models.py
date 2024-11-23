from services.extensions import db


# Modèle pour les oiseaux
class Oiseau(db.Model):
    id_oiseau = db.Column(db.Integer, primary_key=True)
    nom_scientifique = db.Column(db.String(120), unique=True, nullable=False)
    nom_anglais = db.Column(db.String(120), nullable=False)
    nom_français = db.Column(db.String(120), nullable=False)
    lien = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=False)

    chants = db.relationship('Chant', backref='oiseau')

# Modèle pour les enregistrements
class Chant(db.Model):
    id_chant = db.Column(db.Integer, primary_key=True)
    nom_scientifique = db.Column(db.String(120), db.ForeignKey('oiseau.nom_scientifique') ,unique=True, nullable=False)
    chemin_chant = db.Column(db.String(200), nullable=False)
    region = db.Column(db.String(100), nullable=False)

    oiseaux = db.relationship('Oiseau', backref='Chant')


class Liste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    nom = db.Column(db.String(100), nullable=False)

class ListeOiseau(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liste_id = db.Column(db.Integer, db.ForeignKey('liste.id'))
    oiseau_id = db.Column(db.Integer, db.ForeignKey('oiseau.id'))






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