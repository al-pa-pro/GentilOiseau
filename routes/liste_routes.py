import random

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from services.extensions import db
from services.models import Utilisateur, Liste, ListeOiseau, Oiseau, Chant


liste_routes = Blueprint('liste_routes', __name__)


# Afficher les listes d'un utilisateur
@liste_routes.route('/mes_listes')
@login_required
def mes_listes():
    id_utilisateur = session.get('id_utilisateur')
    listes = Liste.query.filter_by(utilisateur_id=id_utilisateur).all()
    return render_template('mes_listes.html', listes=listes)

# Créer une nouvelle liste
@liste_routes.route('/creer_liste', methods=['GET', 'POST'])
@login_required
def creer_liste():
    id_utilisateur = session.get('id_utilisateur')
    print(id_utilisateur)
    if request.method == 'POST':
        nom = request.form['nom']
        nouvelle_liste = Liste(utilisateur_id=id_utilisateur, nom_liste=nom)
        db.session.add(nouvelle_liste)
        db.session.commit()
        flash("Liste créée avec succès.")
        return redirect(url_for('liste_routes.mes_listes'))
    return render_template('mes_listes.html')

# Supprimer une liste
@liste_routes.route('/supprimer_liste/<int:liste_id>', methods=['POST'])
@login_required
def supprimer_liste(liste_id):
    id_utilisateur = session.get('id_utilisateur')
    # Rechercher la liste à supprimer
    liste = Liste.query.filter_by(id_liste=liste_id, utilisateur_id=id_utilisateur).first()
    
    if liste:
        # Supprimer d'abord les oiseaux associés à cette liste dans ListeOiseau
        ListeOiseau.query.filter_by(liste_id=liste_id).delete()
        db.session.commit()  # Appliquer les suppressions des oiseaux associés
        
        # Ensuite, supprimer la liste dans la table Liste
        db.session.delete(liste)
        db.session.commit()
    else:
        flash("Liste introuvable ou vous n'avez pas les droits nécessaires.")
    
    return redirect(url_for('liste_routes.mes_listes'))


@liste_routes.route('/modifier_liste/<int:liste_id>', methods=['GET', 'POST'])
@login_required
def modifier_liste(liste_id):
    id_utilisateur = session.get('id_utilisateur')
    liste=Liste.query.filter_by(id_liste=liste_id).first()
    nom_liste=liste.nom_liste

    # Récupérer la liste des oiseaux associés à cette liste
    liste_oiseaux = ListeOiseau.query.filter_by(liste_id=liste_id).all()

    oiseaux = []
    for lo in liste_oiseaux:
        oiseau = Oiseau.query.get(lo.oiseau_id)
        chants = [{"id_chant": chant.id_chant, "chemin_chant": chant.chemin_chant} for chant in oiseau.chants]
        oiseaux.append({
            "id_oiseau": oiseau.id_oiseau,
            "nom_scientifique": oiseau.nom_scientifique,
            "nom_français": oiseau.nom_français,
            "chants": chants
        })

    # Récupérer la liste des oiseaux disponibles pour ajout (optionnel)
    oiseaux_disponibles = Oiseau.query.all()
    oiseaux_disponibles_list = [{"id_oiseau": o.id_oiseau, "nom_scientifique": o.nom_scientifique, "nom_français": o.nom_français} for o in oiseaux_disponibles]



    return render_template(
        'liste.html',
        liste_id=liste_id,
        nom_liste=nom_liste,
        oiseaux=oiseaux,
        oiseaux_disponibles=oiseaux_disponibles_list,
        id_utilisateur=id_utilisateur
    )

@liste_routes.route('/modifier_nom_liste/<int:liste_id>', methods=['POST'])
@login_required
def modifier_nom_liste(liste_id):
    nouveau_nom = request.form.get('nouveau_nom')
    liste = Liste.query.filter_by(id_liste=liste_id).first()
    
    if liste:
        liste.nom_liste = nouveau_nom
        db.session.commit()
        flash(f"Le nom de la liste a été modifié avec succès.")
    else:
        flash("Liste non trouvée.")
    
    return redirect(url_for('liste_routes.modifier_liste', liste_id))



@liste_routes.route('/oiseau-data', methods=['GET'])
def get_oiseaux():
    region = request.args.get('region')  # Récupère la région depuis les paramètres GET
    query = db.session.query(Oiseau).join(Chant).distinct(Oiseau.nom_scientifique)

    if region:
        query = query.filter(Chant.region == region)

    oiseaux = query.all()
    oiseaux_list = [{"id_oiseau": o.id_oiseau, "nom_scientifique": o.nom_scientifique, "nom_français": o.nom_français} for o in oiseaux]
    return jsonify(oiseaux_list)

@liste_routes.route('/get-chants/<int:oiseau_id>', methods=['GET'])
def get_chants(oiseau_id):
    oiseau = db.session.query(Oiseau).filter_by(id_oiseau=oiseau_id).first()
    
    if not oiseau:
        return jsonify({"error": "Oiseau non trouvé"}), 404

    chants = [{"id_chant": chant.id_chant, "chemin_chant": chant.chemin_chant} for chant in oiseau.chants]
    return jsonify(chants)


@liste_routes.route('/liste/<int:liste_id>/oiseaux', methods=['GET'])
@login_required
def afficher_oiseaux_liste(liste_id):
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


@liste_routes.route('/ajouter_oiseau/<int:liste_id>/<string:nom_scientifique>', methods=['POST'])
@login_required
def ajouter_oiseau(liste_id, nom_scientifique):
    oiseau_selectionné = Oiseau.query.filter_by(nom_scientifique=nom_scientifique).first()
    if oiseau_selectionné:
        oiseau = ListeOiseau(liste_id=liste_id, oiseau_id=oiseau_selectionné.id_oiseau, nom_scientifique=nom_scientifique)
        db.session.add(oiseau)
        db.session.commit()
        flash("Oiseau ajouté à la liste.")
    else:
        flash("Oiseau non trouvé.")
    return redirect(url_for('liste_routes.modifier_liste', liste_id=liste_id))

@liste_routes.route('/supprimer_oiseau/<int:liste_id>/<int:id_oiseau_dans_liste>', methods=['POST'])
@login_required
def supprimer_oiseau_liste(liste_id, id_oiseau_dans_liste):
    # On récupère la relation entre la liste et l'oiseau à partir de la table de jointure
    oiseau = ListeOiseau.query.filter_by(liste_id=liste_id, id_oiseau_dans_liste=id_oiseau_dans_liste).first()

    if oiseau:
        # Si la relation existe, on la supprime de la base de données
        db.session.delete(oiseau)
        db.session.commit()
        flash("Oiseau supprimé de la liste.")
    else:
        # Si aucun oiseau n'est trouvé pour cette liste, on affiche un message d'erreur
        flash("Oiseau non trouvé dans la liste.")
    
    # On redirige l'utilisateur vers la page d'affichage des oiseaux de la liste
    return redirect(url_for('liste_routes.modifier_liste', liste_id=liste_id))



#Route pour générer une liste aleatoirement

@liste_routes.route('/generer_liste', methods=['POST'])
@login_required
def generer_liste():
    region = request.form.get('region')  # Récupérer la région du formulaire
    nombre_oiseau = int(request.form.get('nombre-oiseau'))  # Récupérer le nombre d'oiseaux à ajouter
    nom_liste = request.form.get('nom')  # Récupérer le nom de la liste
    id_utilisateur = session.get('id_utilisateur')  # Utilisateur connecté

    # Filtrer les oiseaux selon la région (s'il y en a une sélectionnée)
    query = Oiseau.query.join(Chant).distinct(Oiseau.nom_scientifique)

    if region:
        query = query.filter(Chant.region == region)  # Appliquer le filtre si une région est sélectionnée

    # Récupérer tous les oiseaux (ou filtrés par région)
    oiseaux_disponibles = query.all()

    # Vérifier si on a assez d'oiseaux
    if len(oiseaux_disponibles) < nombre_oiseau:
        flash("Pas assez d'oiseaux dans la région sélectionnée.")
        return redirect(url_for('liste_routes.mes_listes'))  # Rediriger vers la page de mes listes


    # Sélectionner des oiseaux aléatoires
    oiseaux_aleatoires = random.sample(oiseaux_disponibles, nombre_oiseau)

    # Créer une nouvelle liste pour l'utilisateur
    nouvelle_liste = Liste(nom_liste=nom_liste, utilisateur_id=id_utilisateur)
    db.session.add(nouvelle_liste)
    db.session.commit()  # Sauvegarder la liste avant d'ajouter les oiseaux

    # Ajouter les oiseaux sélectionnés dans la nouvelle liste
    for oiseau in oiseaux_aleatoires:
        liste_oiseau = ListeOiseau(liste_id=nouvelle_liste.id_liste, oiseau_id=oiseau.id_oiseau)
        db.session.add(liste_oiseau)

    db.session.commit()  # Sauvegarder les associations

    flash(f"La liste '{nom_liste}' a été générée avec succès !")
    return redirect(url_for('liste_routes.mes_listes'))  # Rediriger vers la page de mes listes

