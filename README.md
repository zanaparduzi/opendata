Architecture : 
![Architecture](image.png)

Télécharger le dossier à l’adresse : 
https://github.com/zanaparduzi/opendata

Installer les libraries nécessaires : 
pip install -r requirements.txt

Lancer le server mySQL
Dans un terminal SQL exécuter les requêtes que vous trouverez dans le fichier requests.sql pour créer la base de données.

Téléchargez l’application Google Authenticator.
Créer un environnement virtuel  (sur macOS) : 
pip install virtualenv
virtualenv venv
source myenv/bin/activate

Modifier config.py avec les données nécessaires

Lancer l'application avec la ligne de commande :  python app.py
Aller sur l'adresse : 
http://127.0.0.1:5000

Créer un compte : mettre un username et un password
Enregistrer l'OTP donné quelque part (il ne sera plus jamais donné à l'utilisateur)
Enregistrer le QR code sur l'application Google Authenticator (il ne sera jamais redonné à l'utilisateur)
Cliquer sur la bouton "Go to Login Page"
Indiquer username et mot de passe
Indiquer code OTP et code du QR code (récupéré sur Google Authenticator)
Bienvenue sur l'appli !

Les données : 
Liste des coordonnées GPS des monuments nationaux
https://www.data.gouv.fr/fr/datasets/liste-des-coordonnees-gps-des-monuments-nationaux/


