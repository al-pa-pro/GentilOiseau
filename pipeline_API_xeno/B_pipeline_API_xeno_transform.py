import pandas as pd
import os

dict_region={"ile-de-france":"le-de-france","bretagne":"bretagne","normandie":"normandie"}  #à completer

# Charger le fichier CSV
def transform_data(region):
    input_file='0_oiseaux_data_full.csv'
    input_file=  os.path.join(os.path.dirname(__file__), input_file)
    df_oiseaux = pd.read_csv(input_file, sep=";", low_memory=False)

    df_oiseaux["nom_scientifique"] = df_oiseaux["gen"] + " " + df_oiseaux["sp"]

    # Appliquer cette logique à la colonne 'length'
    df_oiseaux['secondes'] = df_oiseaux['length'].apply(lambda x: x.split(":")[1] if isinstance(x, str) else None)
    df_oiseaux['minutes'] = df_oiseaux['length'].apply(lambda x: x.split(":")[0] if isinstance(x, str)  else None)

    # Conversion en nombres (float ou int) en fonction des valeurs
    df_oiseaux['secondes'] = pd.to_numeric(df_oiseaux['secondes'], errors='coerce')
    df_oiseaux['minutes'] = pd.to_numeric(df_oiseaux['minutes'], errors='coerce')

    # Filtrer les données selon vos critères
    mask = (df_oiseaux['minutes'] == 0) & (df_oiseaux['secondes'] >= 5) & (df_oiseaux['secondes'] <= 20)  & (df_oiseaux['gen'] != "Mystery") & df_oiseaux['loc'].str.contains(dict_region[region], case=False, na=False) & (df_oiseaux['q'] == "A")
    df_oiseaux_transformed = df_oiseaux[mask]


    # Enregistrer les données dans un fichier CSV 
    output_file = f"1_oiseaux_data_{region}.csv"
    output_file=  os.path.join(os.path.dirname(__file__), output_file)
    df_oiseaux_transformed.to_csv(output_file, index=False, sep=";",encoding='utf-8')
    print(f"Les données ont été enregistrées dans le fichier : {output_file}")

    #affichage des informations
    print(df_oiseaux_transformed.head())  # Affiche la première ligne
    print(df_oiseaux.info())
    return()

#transform_data("bretagne")