import requests

# URL d'exemple
url = "https://xeno-canto.org/883856/download"

try:
    # Envoyer une requête HEAD pour obtenir les en-têtes
    response = requests.head(url, allow_redirects=True)
    
    # Afficher tous les en-têtes HTTP
    print("En-têtes de la réponse HTTP :")
    for header, value in response.headers.items():
        print(f"{header}: {value}")
        
except requests.RequestException as e:
    print(f"Erreur lors de la requête : {e}")