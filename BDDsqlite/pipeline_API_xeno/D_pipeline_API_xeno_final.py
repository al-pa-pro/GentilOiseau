import pandas as pd
import os

def data_final(region):
    # Charger le fichier CSV avec les liens de téléchargement
    input_file=f'2_oiseaux_data_{region}_type.csv'
    input_file= os.path.join(os.path.dirname(__file__), input_file)
    df = pd.read_csv(input_file, sep=";", low_memory=False)  

    
    df_final = df[(df['type_fichier'] == "MP3")]
    

    # Enregistrer les données dans un fichier CSV 
    output_file = f"3_oiseaux_data_{region}_final.csv"
    output_file=  input_file= os.path.join(os.path.dirname(__file__), output_file)
    df_final.to_csv(output_file, index=False, sep=";",encoding='utf-8')
    print(f"Les données ont été enregistrées dans le fichier : {output_file}")
    return()


#data_final("bretagne")