------------------------------------------
Partie Développement web

Comment installer le projet ?

1)Exécutez votre serveur local (Ex : Wamp) .

2)Insérez la base de données "projet3" dans votre gestionnaire de base de données
MySQL nommé schema.sql se trouvant dans le répertoire projet3/sql/schema.sql.
/!\En cas d'erreur innatendue, un fichier schema_neutre.sql est disponible, sans les données de test dans la base de données

3)Exécutez le fichier app.py à l'aide de python dans le répertoire projet3/app.py dans votre terminal
ou dans un environnement de développement intégré .

4)Ouvrez votre navigateur web et écrivez dans votre barre d'adresse localhost:5000 .

5)Le site web est fonctionnel !


Pour modifier les informations servant à se connecter au serveur MySQL :
1) Ouvrir le fichier config.json dans le répertoire projet3/config.json .

{
    "MYSQL_DATABASE_USER": "Votre nom d'utilisateur",
    "MYSQL_DATABASE_PASSWORD": "Votre mot de passe",
    "MYSQL_DATABASE_DB": "Insérez le nom de la base de données",
    "MYSQL_DATABASE_HOST": "localhost",
    "MYSQL_DATABASE_PORT": 3306
}


La base de données possède comme valeurs par défaut :
{
    "MYSQL_DATABASE_USER": "root",
    "MYSQL_DATABASE_PASSWORD": "",
    "MYSQL_DATABASE_DB": "projet3",
    "MYSQL_DATABASE_HOST": "localhost",
    "MYSQL_DATABASE_PORT": 3306
}


Bibliothèques utilisées :
-Flask
-Flask-MySQL
-PyMySQL
-mysql-connector-python
-Os (module)


------------------------------------------
Partie Intégration Multimédia

Les fichiers .html se trouvent dans le répertoire projet/templates .
Les fichiers .css se trouvent dans le répertoire projet/static .

Les fichiers .html ont été validées par https://validator.w3.org/ .
Cependant des erreurs apparaissent à cause d'un conflit HTML / Jinja .
Les fichiers .css ont été validées par https://jigsaw.w3.org/css-validator/ .

------------------------------------------

Comment utiliser le site :

-Formulaire d'envoi d'image 🔑 => Bouton Publier qui n'apparait que en étant connecté ✅

-Affichage d'une section sur la page d'accueil comportant un sous-ensemble d'images ✅
aléatoires envoyées au site web => Accueil ou logo ✅

-Page affichant toutes les images envoyées triées par ordre décroissant de date
de mise en ligne (c’est-à-dire de la plus récente à la plus ancienne) => Galerie ✅

-Page affichant le détail de l'image (nom du créateur, date de mise en ligne et titre
de l'image) => Cliquer sur une image ✅

-Page affichant les images d'un créateur => Cliquer sur le nom d'un créateur dans le détail de l'image

-Formulaire de connexion (avec pseudonyme et mot de passe) => Se connecter✅

-Lien ou formulaire de déconnexion 🔑 => Se déconnecter ✅

-Formulaire d'inscription => S'inscrire ✅

-Affichage des commentaires d'une image	=> Sur la page image et cliquer sur un commentaire pour afficher les détails ✅

-Formulaire d'ajout d'un commentaire sur une image 🔑 => Être connecté et être sur la page image ✅

-Formulaire de suppression d'un commentaire sur une image 🔐 => Accéder au détail d'une image et bouton supprimer
(Il faut être l'auteur du commentaire) ✅

-Formulaire de modification d'un commentaire sur une image 🔐 => Accéder au détail d'une image et bouton modifier
(Il faut être l'auteur du commentaire) ✅

-Formulaire de suppression d'une image 🔐 => Être connecté et être sur la page image puis bouton supprimer en dessous de l'image
(Il faut être le créateur de l'image) ✅

-Ajout d'un cœur sur une image 🔑 => ❌	
		
-Suppression d'un cœur sur une image 🔐 => ❌

-Affichage d'une section sur la page d'accueil comportant les images les plus
populaires (c’est-à-dire ayant le plus de cœurs). Le nombre d'images populaires à
afficher est le même que le nombre d'images aléatoires à afficher => ❌	
		
-Gestion du partage de vidéos (et d'audios) => Le site prend en compte les vidéos et les audios ✅
