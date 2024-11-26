import random

from flask_login import login_required
from flask import jsonify, request, render_template, Blueprint, session
from services.models import Oiseau, Chant, Liste, ListeOiseau
from services.extensions import db

quiz_routes = Blueprint('quiz_routes', __name__)

@quiz_routes.route('/quiz')
def quiz():
    listes_publiques = Liste.query.filter_by(status="public").all()  # Récupère les listes publiques
    if "id_utilisateur" in session:
        id_utilisateur = session.get('id_utilisateur')
        listes_personnelles = Liste.query.filter_by(utilisateur_id=id_utilisateur).all()  # Récupère les listes publiques
        return render_template('quiz.html', listes_publiques=listes_publiques,listes_personnelles=listes_personnelles)

    return render_template('quiz.html', listes_publiques=listes_publiques)

@quiz_routes.route('/quiz-data', methods=['GET'])
def get_oiseaux():
    region = request.args.get('region')  # Récupère la région depuis les paramètres GET
    liste_id = request.args.get('liste_id')  # Récupère la région depuis les paramètres GET
    print(liste_id)
    query = db.session.query(Oiseau).join(Chant).distinct(Oiseau.nom_scientifique)

    if region:
        query = query.filter(Chant.region == region)

    if liste_id:
        query=query.join(ListeOiseau).filter(ListeOiseau.liste_id==liste_id)
    
    oiseaux = query.all()
    oiseaux_list = [{"id_oiseau": o.id_oiseau, "nom_scientifique": o.nom_scientifique, "nom_français": o.nom_français} for o in oiseaux]
    return jsonify(oiseaux_list)

@quiz_routes.route('/get-chants/<int:oiseau_id>', methods=['GET'])
def get_chants(oiseau_id):
    # Récupère l'oiseau par son ID
    oiseau = db.session.query(Oiseau).filter_by(id_oiseau=oiseau_id).first()
    
    if not oiseau:
        return jsonify({"error": "Oiseau non trouvé"}), 404

    # Récupère tous les chants associés à cet oiseau
    chants = [{"id_chant": chant.id_chant, "chemin_chant": chant.chemin_chant} for chant in oiseau.chants]
    
    return jsonify(chants)


@quiz_routes.route('/quiz-random', methods=['GET'])
def random_quiz():
    # Récupérer la région de la requête, ou None si pas spécifiée
    region = request.args.get('region')

    # Si une région est spécifiée, filtrer par région, sinon récupérer tous les oiseaux
    if region:
        oiseaux = db.session.query(Oiseau).join(Chant).filter(Chant.region == region).distinct(Oiseau.nom_scientifique).all()
    else:
        oiseaux = db.session.query(Oiseau).join(Chant).distinct(Oiseau.nom_scientifique).all()

    # Si vous voulez limiter la sélection à 10 oiseaux aléatoires, utilisez random.sample
    random_selection = random.sample(oiseaux, min(len(oiseaux), 10))

    # Créer les données pour le quiz
    quiz_data = [{"id_oiseau": o.id_oiseau, "nom_scientifique": o.nom_scientifique, "nom_français": o.nom_français} for o in random_selection]

    return jsonify(quiz_data)



@quiz_routes.route('/start-quiz', methods=['POST'])
def start_quiz():
    # Récupérer les IDs des oiseaux sélectionnés et les paramètres supplémentaires
    data = request.get_json()
    oiseaux_ids = data.get('selected_ids', [])
    num_questions = int(data.get('num_questions', 5))  # Nombre de questions, par défaut 5
    num_options = int(data.get('num_options', 3))  # Nombre de possibilités, par défaut 3

    # Récupérer les oiseaux sélectionnés dans la liste
    oiseaux_selectionnes = db.session.query(Oiseau).filter(Oiseau.id_oiseau.in_(oiseaux_ids)).all()

    # S'assurer qu'il y a suffisamment d'oiseaux pour le nombre de questions
    oiseaux_corrects = random.sample(oiseaux_selectionnes, min(num_questions, len(oiseaux_selectionnes)))

    quiz_questions = []
    for o in oiseaux_corrects:
        # Récupère un enregistrement aléatoire pour l'oiseau
        chant = random.sample(o.chants, 1)[0]
        
        # Crée une question avec des choix aléatoires parmi les oiseaux sélectionnés
        autres = [o]  # On commence par inclure l'oiseau actuel dans la liste des choix
        while len(autres) < num_options:  # On veut 'num_options' choix
            autre_oiseau = random.choice([oi for oi in oiseaux_selectionnes if oi != o])
            if autre_oiseau not in autres:  # Pour éviter les doublons
                autres.append(autre_oiseau)
        
        # Construire les choix à afficher (l'oiseau actuel et les autres)
        choix = [{"nom_scientifique": o.nom_scientifique, "nom_français": o.nom_français, "id_oiseau": o.id_oiseau, "correct": True}] + [
            {"nom_scientifique": a.nom_scientifique, "nom_français": a.nom_français, "id_oiseau": a.id_oiseau, "correct": False} for a in autres[1:]
        ]
    
        # Mélange des options pour chaque question
        random.shuffle(choix)  # Mélange les options

        quiz_questions.append({
            "audio": chant.chemin_chant,
            "correct_name": o.nom_français,  # Bonne réponse ajoutée ici
            "options": random.sample(choix, len(choix)),  # Mélange les options
        })

    return jsonify(quiz_questions)





@quiz_routes.route('/quiz/<int:liste_id>/oiseaux', methods=['GET'])
def afficher_oiseaux_quiz(liste_id):
    liste_oiseaux = ListeOiseau.query.filter_by(liste_id=liste_id).all()
    oiseaux = []
    for lo in liste_oiseaux:
        oiseau = Oiseau.query.get(lo.oiseau_id)
        chants = [{"id_chant": chant.id_chant, "chemin_chant": chant.chemin_chant} for chant in oiseau.chants]
        oiseaux.append({
            "id_oiseau_dans_liste": lo.id_oiseau_dans_liste,
            "id_oiseau": oiseau.id_oiseau,
            "nom_scientifique": oiseau.nom_scientifique,
            "nom_français": oiseau.nom_français,
            "chants": chants
        })
    return jsonify(oiseaux)





