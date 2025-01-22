import requests
import pandas as pd
import os

def oiseaux_data():
    # Utilisation d'un mot-clé pour récupérer les oiseaux en France
    species_query = requests.utils.quote("cnt:france")
    base_url = f"https://www.xeno-canto.org/api/2/recordings?query={species_query}"
    
    all_recordings = []  # Liste pour stocker toutes les données récupérées
    page = 1  # Initialiser la page
    
    try:
        while True and page <= 200:  # Limiter à 125 pages
            # Ajouter le numéro de page à l'URL
            paged_url = f"{base_url}&page={page}"
            response = requests.get(paged_url)
            print(f"Statut de la réponse (Page {page}): {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                recordings = data["recordings"]
                print(f"Nombre d'enregistrements récupérés sur la page {page}: {len(recordings)}")
                
                if not recordings:  # Si aucun enregistrement, arrêter la boucle
                    print(f"Aucun enregistrement sur la page {page}, arrêt de la récupération.")
                    break
                
                # Ajouter les enregistrements à la liste globale
                all_recordings.extend(recordings)
                page += 1  # Passer à la page suivante
            else:
                print(f"Erreur lors de la récupération des données (Page {page}): {response.text}")
                break
        
        # Afficher le nombre total d'enregistrements récupérés
        print("Nombre total d'enregistrements récupérés :", len(all_recordings))
        
        # Charger les données complètes dans un DataFrame
        df_oiseaux = pd.DataFrame(all_recordings)
        print("Nombre total d'enregistrements dans le DataFrame:", len(df_oiseaux))
        
        # Afficher un exemple de ligne de données
        print("Exemple de ligne de données :")
        print(df_oiseaux.head())  # Affiche la première ligne
        
        # Enregistrer les données dans un fichier CSV avec un séparateur spécifié
        output_file = "0_oiseaux_data_full.csv"
        output_file=  os.path.join(os.path.dirname(__file__), output_file)
        df_oiseaux.to_csv(output_file, index=False, sep=';', encoding='utf-8')
        print(f"Les données ont été enregistrées dans le fichier : {output_file}")
        
        return df_oiseaux
    except requests.exceptions.RequestException as e:
        print("Erreur de connexion :", e)

# Exécute la fonction pour tester
#df_oiseaux = oiseaux_data()
