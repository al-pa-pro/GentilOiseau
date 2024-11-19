import pandas as pd
import requests
import os

def add_type(region):
    # Charger le fichier CSV avec les liens de téléchargement
    input_file=f'1_oiseaux_data_{region}.csv'
    print(input_file)
    input_file=  input_file= os.path.join(os.path.dirname(__file__), input_file)
    df = pd.read_csv(input_file, sep=";", low_memory=False)  
    df['type_fichier'] = ''  # Ajouter une colonne pour stocker le type de fichier

    for index, row in df.iterrows():
        url = row['file']  
        
        try:
            # Envoyer une requête HEAD pour obtenir les en-têtes
            response = requests.head(url, allow_redirects=True)
            
            # Analyser l'en-tête Content-Type pour déterminer le type de fichier
            content_type = response.headers.get('Content-Type', '')
            if 'audio/mpeg' in content_type:
                df.at[index, 'type_fichier'] = 'MP3'
            elif 'audio/wav' in content_type:
                df.at[index, 'type_fichier'] = 'WAV'
            else:
                df.at[index, 'type_fichier'] = 'Inconnu'
            
            print(f"URL : {url} - Type de fichier : {df.at[index, 'type_fichier']}")

        except requests.RequestException as e:
            print(f"Erreur avec l'URL : {url} - {e}")

    # Sauvegarder les résultats dans un nouveau fichier CSV
    output_file =f'2_oiseaux_data_{region}_type.csv'
    output_file = os.path.join(os.path.dirname(__file__), output_file)
    df.to_csv(output_file, index=False, sep=";",)
    print(f"Analyse des en-têtes terminée. Résultats enregistrés dans {output_file}")
    return()

#add_type("bretagne")