import pandas as pd
import os
import requests
import sqlite3



def traduction():

    bdd_path= os.path.join(os.path.dirname(os.path.dirname(__file__)), 'BDDsqlite', 'oiseaux.db')
    print(bdd_path)

    with sqlite3.connect(bdd_path) as conn:

        cursor = conn.cursor()



        # Charger le fichier CSV avec les liens de téléchargement
        input_file=f'traduction.xlsx'
        input_file = os.path.join(os.path.dirname(__file__), input_file)
        print(input_file)


        # Lecture du fichier CSV dans un DataFrame
        df = pd.read_excel(input_file, engine='openpyxl')


        # Récupération des noms scientifique, nom anglais et nom français
        for index, row in df.iterrows():
            nom_scientifique = row["IOC14.2"]
            nom_anglais = row["English"]
            nom_francais = row["French"]

            cursor.execute(""" INSERT INTO oiseau (nom_scientifique, nom_anglais, nom_français)
                    VALUES (?, ?, ?)""", (nom_scientifique, nom_anglais, nom_francais))
    
    conn.commit()

    print("insertion terminé.")
    return()

traduction()
