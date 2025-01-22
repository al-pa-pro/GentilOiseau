I) Pour faire tourner le site sur sa machine

Le site n'est plus en ligne depuis décembre 2024.

Pour faire tourner le site intégralement sur votre machine, deux options s'offrent à vous :

Revenir à la version de novembre 2024 (utilisant SQLite) :
Cette version est disponible dans le répertoire GitHub du projet. Vous pouvez la cloner à l'aide du lien suivant : [Lien GitHub]
Dans ce cas, il vous faudra installer Python et les librairies listées dans le fichier requirements.txt. Vous devrez également créer vous-même un fichier .env contenant une SECRET_KEY (par exemple, "secret_key"), un MAIL_USERNAME et un MAIL_PASSWORD.

Revenir à la version de janvier 2025 qui utilise Docker avec PostgreSQL :
Cette version est disponible dans le répertoire GitHub du projet. Vous pouvez la cloner à l'aide du lien suivant : [Lien GitHub]
Pour cette option, vous devrez construire l'environnement à partir du fichier docker-compose.yaml. Là aussi, il vous faudra un fichier .env contenant une SECRET_KEY, un MAIL_USERNAME, un MAIL_PASSWORD, et des identifiants pour PostgreSQL et pgAdmin (POSTGRES_USER, POSTGRES_PASSWORD, PGADMIN_DEFAULT_EMAIL, PGADMIN_DEFAULT_PASSWORD). Ensuite, dans Docker Desktop, accédez au conteneur de l'application (python_app) et exécutez la commande de migration pour importer les données de la BDD SQLite :
"python migration.py" ou "docker exec python migration.py"




II) Le projet

Le site est un projet autodidacte permettant l'apprentissage des chants d'oiseaux. Il est disponible sur gentiloiseau.onrender.com jusqu'à fin décembre. Comme il s'agit d'un hébergeur gratuit, il faut attendre 30 secondes avant le démarrage du serveur et l'affichage du site.

Le site est probablement encore en partie immature et mérite des retours pour son amélioration, que ce soit pour l'utilisation ou pour le code.



Les technologies utilisées pour sa création sont les suivantes :

1) Coding : Visual Studio Code + environnement virtuel  

2) Python : SQLAlchemy, Flask, Flask-Mail, Flask-Login 

3) SQL : SQLite (pour le développement), PostgreSQL (pour la production)  

4) Versioning : Git / GitHub  

5) Mise en ligne : Render  (de novembre 2024 à décembre 2024)

6) Méthode : Programmation Orientée Objet, Programmation Fonctionnelle
  
7) Front : HTML / CSS / JavaScript  

8) conteneurisation : Docker



Sous-projets élaborés :

Pipeline ETL pour récupérer les chants d'oiseaux (en les extrayant via l'API de xeno-canto). Voir le dossier pipeline_API_xeno.  

Mise en place d'une fonctionnalité de quiz pour les chants d'oiseaux.

Mise en place de fonctionnalités pour les utilisateurs (inscription, connexion, récupération de mot de passe, création de liste personnalisée).
Contrairement à mon dernier projet, je n'ai inséré ni tests unitaires (pytest) ni logging, car ce projet est beaucoup plus simple et visait à être opérationnel rapidement (mise en place en 2 semaines). De même, je n'ai pas utilisé d'outils comme autopep8. Cependant, il est possible que ces éléments soient ajoutés dans un futur proche.

