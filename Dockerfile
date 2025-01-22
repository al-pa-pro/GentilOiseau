# Utilise une image Python officielle comme base
FROM python:3.11

# Définit un répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier requirements.txt et installe les dépendances
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copie l'ensemble du code dans le répertoire de travail
COPY . /app/

# Expose le port sur lequel l'application écoute
EXPOSE 5000

# Commande pour démarrer ton application Python (par exemple avec Flask)
CMD ["python", "app.py"]