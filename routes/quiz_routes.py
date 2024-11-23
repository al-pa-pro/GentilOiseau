import random

from flask import jsonify, request, render_template, Blueprint
from services.models import Oiseau, Chant
from services.extensions import db

quiz_routes = Blueprint('quiz_routes', __name__)

@quiz_routes.route('/quiz-data', methods=['GET'])
def get_oiseaux():
    region = request.args.get('region')  # Récupère la région depuis les paramètres GET
    query = db.session.query(Oiseau).join(Chant).distinct(Oiseau.nom_scientifique)

    if region:
        query = query.filter(Chant.region == region)

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
    oiseaux = db.session.query(Oiseau).join(Chant).distinct(Oiseau.nom_scientifique).all()
    random_selection = random.sample(oiseaux, min(len(oiseaux), 10))
    quiz_data = [{"id_oiseau": o.id_oiseau, "nom_scientifique": o.nom_scientifique, "nom_français": o.nom_français} for o in random_selection]
    return jsonify(quiz_data)

@quiz_routes.route('/start-quiz', methods=['POST'])
def start_quiz():
    oiseaux_ids = request.json.get('selected_ids', [])
    #recupération des oiseaux selectionnés dans la liste
    oiseaux_selectionnes = db.session.query(Oiseau).filter(Oiseau.id_oiseau.in_(oiseaux_ids)).all()

    # 5 questions
    oiseaux_corrects=random.sample(oiseaux_selectionnes, min(5, len(oiseaux_selectionnes)))

    quiz_questions = []
    for o in oiseaux_corrects:
        # Récupère un enregistrement aléatoire pour l'oiseau
        chant = random.sample(o.chants, 1)[0]
        
        # Crée une question avec des choix aléatoires parmi les 5 oiseaux sélectionnés
        autres = []  # On commence par inclure l'oiseau actuel dans la liste des choix
        limit=0
        while len(autres) < 3:  # On veut 3 options, dont l'oiseau actuel et 2 autres oiseaux au hasard parmi les 5
            limit=limit+1
            # Choisir un oiseau parmi ceux déjà sélectionnés, mais qui n'est pas l'oiseau actuel
            autre_oiseau = random.choice([oi for oi in oiseaux_selectionnes if oi != o])
            if autre_oiseau not in autres:  # Pour éviter les doublons
                autres.append(autre_oiseau)
            if limit >10:
                break
    

        # Construire les choix à afficher (l'oiseau actuel et 2 autres oiseaux)
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


