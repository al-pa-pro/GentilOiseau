import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.models import Oiseau, Chant, Liste, ListeOiseau, Utilisateur  # Assurez-vous que ces modèles sont définis correctement

load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Connexion à la base de données SQLite
sqlite_engine = create_engine('sqlite:///' + os.path.join(os.path.dirname(__file__), 'BDDsqlite', 'oiseaux.db'))
SQLiteSession = sessionmaker(bind=sqlite_engine)

# Connexion à la base de données PostgreSQL
postgresql_engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}')
PostgresqlSession = sessionmaker(bind=postgresql_engine)

# Fonction pour migrer les données de SQLite vers PostgreSQL
def migrate_data():
    # Utilisation des gestionnaires de contexte pour les sessions
    with SQLiteSession() as sqlite_session, PostgresqlSession() as postgresql_session:
        try:
            # Créer les tables dans PostgreSQL si elles n'existent pas encore
            # Ceci crée toutes les tables définies dans le modèle (ex: Oiseau, Chant, etc.)
            Oiseau.metadata.create_all(postgresql_engine)
            Chant.metadata.create_all(postgresql_engine)
            Utilisateur.metadata.create_all(postgresql_engine)
            Liste.metadata.create_all(postgresql_engine)
            ListeOiseau.metadata.create_all(postgresql_engine)

            # Récupérer les données depuis SQLite
            oiseau_data = sqlite_session.query(Oiseau).all()
            chant_data = sqlite_session.query(Chant).all()
            

            # Insérer les données dans PostgreSQL
            for oiseau in oiseau_data:
                pg_oiseau = Oiseau(
                    nom_scientifique=oiseau.nom_scientifique,
                    nom_anglais=oiseau.nom_anglais,
                    nom_français=oiseau.nom_français,
                    lien=oiseau.lien,
                    image=oiseau.image
                )
                postgresql_session.add(pg_oiseau)

            for chant in chant_data:
                pg_chant = Chant(
                    nom_scientifique=chant.nom_scientifique,
                    chemin_chant=chant.chemin_chant,
                    region=chant.region
                )
                postgresql_session.add(pg_chant)


            # Commit des changements dans PostgreSQL
            postgresql_session.commit()
            print("Migration des données terminée avec succès !")
        
        except Exception as e:
            postgresql_session.rollback()  # Annule les transactions en cas d'erreur
            print(f"Erreur lors de la migration des données : {e}")

# Migrer les données
migrate_data()
