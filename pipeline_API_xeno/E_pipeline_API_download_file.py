import pandas as pd
import os
import requests
import sqlite3



def download_file(region):

    bdd_path= os.path.join(os.path.dirname(os.path.dirname(__file__)), 'BDDsqlite', 'oiseaux.db')
    print(bdd_path)

    with sqlite3.connect(bdd_path) as conn:

        cursor = conn.cursor()



        # Charger le fichier CSV avec les liens de téléchargement
        input_file=f'3_oiseaux_data_{region}_final.csv'
        input_file = os.path.join(os.path.dirname(__file__), input_file)
        print(input_file)

        # Chemin du dossier de destination
        output_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static','uploads',f'{region}')
        print(output_folder)

        # Création du dossier s'il n'existe pas
        os.makedirs(output_folder, exist_ok=True)

        # Lecture du fichier CSV dans un DataFrame
        df = pd.read_csv(input_file, sep=";", low_memory=False)
        df["nom_scientifique"] = df["gen"] + " " + df["sp"]

        # Vérification si la colonne "file" existe
        if "file" not in df.columns:
            raise ValueError("La colonne 'file' n'existe pas dans le fichier CSV.")

        # Téléchargement des fichiers depuis les liens dans la colonne "file"
        for index, row in df.iterrows():
            try:
                # Récupération des valeurs de la ligne courante
                url = row["file"]
                id_audio = str(row["id"])
                nom_scientifique = row["nom_scientifique"]
                response = requests.get(url, stream=True)
                response.raise_for_status()  # Vérifie si la requête a réussi

                output_file = os.path.join(output_folder, f"{id_audio}.mp3")

                # Sauvegarde du fichier téléchargé
                with open(output_file, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

                print(f"Fichier sauvegardé : {output_file}")

                cursor.execute(""" INSERT INTO audio (region, nom_scientifique, chemin_audio)
                    VALUES (?, ?, ?)""", (region, nom_scientifique, output_file))

            except Exception as e:
                print(f"Erreur lors du téléchargement du fichier {url}: {e}")
            
    conn.commit()

    print("Téléchargement terminé.")
    return()

#download_file("bretagne")