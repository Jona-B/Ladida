from flask import Flask, session, redirect, request, render_template, url_for, send_from_directory
from flaskext.mysql import MySQL
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from pymysql.cursors import DictCursor
from os import getcwd
from os.path import join
from uuid import uuid4
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'KfKkH48u1FZ24_r#g'
config_path = os.path.join(app.root_path, 'config.json')

mysql = MySQL()
mysql.init_app(app)

#Accueil
@app.route('/')
def affiche_accueil():
    connexion = mysql.connect() #Ouvre une connexion au serveur SQL
    curseur = connexion.cursor(cursor=DictCursor) 
    curseur.execute('SELECT nom FROM image WHERE type_fichier = "image" ORDER BY RAND()') #Galerie d'images du plus récent au plus ancien
    dictionnaires_images = curseur.fetchmany(3) #Limiter le nombres d'images à 3 sur l'accueil
    curseur.execute('SELECT nom FROM image WHERE type_fichier = "video" ORDER BY RAND()') #Galerie d'images du plus récent au plus ancien
    dictionnaires_videos = curseur.fetchmany(2) #Limiter le nombres de vidéos à 2 sur l'accueil
    curseur.execute('SELECT nom FROM image WHERE type_fichier = "audio" ORDER BY RAND()') #Galerie d'images du plus récent au plus ancien
    dictionnaires_audios = curseur.fetchmany(1) #Limite le nombre de fichier audio à 1
    curseur.close()
    connexion.close()
    return render_template('accueil.html', dictionnaires_images=dictionnaires_images, dictionnaires_videos=dictionnaires_videos, dictionnaires_audios=dictionnaires_audios)
#Espace Membre

@app.route('/inscription', methods=['GET','POST'])
def inscription():
    if request.method == 'POST':
        connexion = mysql.connect()
        curseur = connexion.cursor()
        pseudonyme = request.form['pseudonyme'] #Récupère la donnée du formulaire 
        mot_de_passe = request.form['mot_de_passe']
        curseur.execute('SELECT pseudonyme FROM membre WHERE pseudonyme = %s', (pseudonyme))
        dictionnaire_membre = curseur.fetchone()
        if dictionnaire_membre != None: #Si l'utilisateur existe déjà, on renvoie un message d'erreur
            curseur.close()
            connexion.close()
            return render_template('erreur_inscription.html')
        else: #Si le membre n'existe pas encore, on insère les données dans la base de données
            curseur.execute('INSERT INTO membre (pseudonyme, mot_de_passe_chiffre) VALUES (%s, %s)', (pseudonyme, generate_password_hash(mot_de_passe)))
            curseur.close()
            connexion.commit()
            connexion.close()
            return render_template('inscription_validee.html')
    return render_template('inscription.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        connexion = mysql.connect()
        curseur = connexion.cursor(cursor=DictCursor)
        pseudonyme = request.form['pseudonyme']
        mot_de_passe = request.form['mot_de_passe']
        curseur.execute('SELECT pseudonyme, mot_de_passe_chiffre FROM membre WHERE pseudonyme = %s', (pseudonyme))
        dictionnaire_membre = curseur.fetchone()
        #Si le pseudo entré n'existe pas ou mot de passe incorrect, mesage d'erreur
        if dictionnaire_membre == None or check_password_hash(dictionnaire_membre['mot_de_passe_chiffre'], mot_de_passe) == False:
            return render_template('erreur_de_connexion.html')
        else: #Si c'est bon, on ouvre une session au nom du pseudonyme 
            session['pseudonyme'] = request.form['pseudonyme']
            return redirect('/')
    return render_template('connexion.html')

@app.route('/deconnexion')
def deconnexion():
    if 'pseudonyme' in session:#Si on est connecté, cela ferme la session
        del session['pseudonyme']
    return redirect('/')

#Image
EXTENSIONS_AUTORISEES = ['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3'] #Formats autorisés
app.config['UPLOAD_FOLDER'] = join(getcwd(), 'images_envoyees') #Envoi vers le dossier images_envoyees

def extension_autorisee(nom_du_fichier):
    return '.' in nom_du_fichier and \
        nom_du_fichier.rsplit('.', 1)[1].lower() in EXTENSIONS_AUTORISEES

@app.route('/formulaire')
def affiche_formulaire_envoi_image():
    return render_template('formulaire_envoi_image.html')

@app.route('/envoie-image', methods = ['POST'])
def envoie_image():
    fichier = request.files['image_utilisateur']
    if extension_autorisee(fichier.filename):
        nom_de_fichier = secure_filename(fichier.filename)
        fichier.save(join(app.config['UPLOAD_FOLDER'], nom_de_fichier))
        createur = request.form['createur']
        titre = request.form['titre']
        connexion = mysql.connect()
        curseur = connexion.cursor()
        extension=nom_de_fichier.split('.')[-1]#Permet de récupérer l'extension d'un fichier 
        if str(extension) == 'mp4': #Selon l'extension , j'insère dans la base de données le type de fichier
            format_fichier = "video"
        elif str(extension) == 'mp3':
            format_fichier = "audio"
        else:
            format_fichier = "image"
        curseur.execute('INSERT INTO image (nom, createur, titre, type_fichier) VALUES (%s, %s, %s, %s)', (nom_de_fichier , createur, titre, format_fichier))  #Inserer dans la table image les informations demandées
        curseur.close()
        connexion.commit()
        connexion.close()
        return redirect(url_for('affiche_page_image', nom_image = nom_de_fichier ))
    else:
        return render_template('erreur_envoi_image.html')

@app.route('/page-image')
def affiche_page_image():
    nom_image = request.args['nom_image'] #récupère le paramètre nom_image dans l'url
    connexion = mysql.connect()
    curseur = connexion.cursor()
    curseur.execute('SELECT id, contenu, auteur, date_mise_en_ligne FROM commentaire WHERE image = %s ORDER BY date_mise_en_ligne DESC', (nom_image))
    commentaires = curseur.fetchall() #Créer un tuples 
    curseur.close()
    curseur = connexion.cursor(cursor=DictCursor) #Créer un dictionnaire
    curseur.execute('SELECT createur, date_mise_en_ligne, titre, type_fichier FROM image WHERE nom = %s', (nom_image))
    dictionnaire_image = curseur.fetchone() 
    curseur.close()
    connexion.close()
    if dictionnaire_image["type_fichier"] == 'image': #En fonction du type de fichier récupéré dans la base de données , on ouvre la bonne page html 
        return render_template('image.html', commentaires = commentaires, titre=dictionnaire_image['titre'], nom_image=nom_image, createur=dictionnaire_image['createur'], date_mise_en_ligne=dictionnaire_image['date_mise_en_ligne'])
    elif dictionnaire_image["type_fichier"] == 'video':
        return render_template('video.html', commentaires = commentaires, titre=dictionnaire_image['titre'], nom_image=nom_image, createur=dictionnaire_image['createur'], date_mise_en_ligne=dictionnaire_image['date_mise_en_ligne'])
    else:
        return render_template('audio.html', commentaires = commentaires, titre=dictionnaire_image['titre'], nom_image=nom_image, createur=dictionnaire_image['createur'], date_mise_en_ligne=dictionnaire_image['date_mise_en_ligne'])
@app.route('/image')
def affiche_image():
    nom_image = request.args['nom_image']
    return send_from_directory(app.config['UPLOAD_FOLDER'], nom_image)

@app.route('/galerie')
def affiche_galerie():
    connexion = mysql.connect()
    curseur = connexion.cursor(cursor=DictCursor)
    #On sélectionne les fichiers d'un même type dans la base de données , puis les incrémentes dans des dictionnaires
    curseur.execute('SELECT nom FROM image WHERE type_fichier = "image" ORDER BY date_mise_en_ligne DESC') #Galerie d'images du plus récent au plus ancien
    dictionnaires_images = curseur.fetchall()
    curseur.execute('SELECT nom FROM image WHERE type_fichier = "video" ORDER BY date_mise_en_ligne DESC') #Galerie d'images du plus récent au plus ancien
    dictionnaires_videos = curseur.fetchall()
    curseur.execute('SELECT nom, titre FROM image WHERE type_fichier = "audio" ORDER BY date_mise_en_ligne DESC') #Galerie d'images du plus récent au plus ancien
    dictionnaires_audios = curseur.fetchall()
    connexion.close()
    return render_template('galerie.html', dictionnaires_images=dictionnaires_images, dictionnaires_videos=dictionnaires_videos, dictionnaires_audios=dictionnaires_audios)

@app.route('/image_createur')
def affiche_image_createur():
    createur = request.args['createur']
    connexion = mysql.connect()
    curseur = connexion.cursor(cursor=DictCursor)
    #On récupère les fichiers d'une personne en particulier avec WHERE createur="%s"
    curseur.execute('SELECT nom FROM image WHERE type_fichier = "image" AND createur = %s' , (createur)) #Afficher les images d'un créateur sur une page
    dictionnaires_images = curseur.fetchall()
    curseur.execute('SELECT nom FROM image WHERE type_fichier = "video" AND createur = %s' , (createur)) #Afficher les images d'un créateur sur une page
    dictionnaires_videos = curseur.fetchall()
    curseur.execute('SELECT nom FROM image WHERE type_fichier = "audio" AND createur = %s' , (createur)) #Afficher les images d'un créateur sur une page
    dictionnaires_audios = curseur.fetchall()
    return render_template('image_createur.html',dictionnaires_videos = dictionnaires_videos,  dictionnaires_audios = dictionnaires_audios, dictionnaires_images=dictionnaires_images, createur = createur)

@app.route('/supprimer')
def supprimer_image_createur():
    nom_image = request.args['nom_image']
    connexion = mysql.connect()
    curseur = connexion.cursor(cursor=DictCursor)
    img_path = ("images_envoyees/" + str(nom_image))
    curseur.execute('DELETE FROM image WHERE nom = %s', (nom_image)) #Supprime les informations de l'image dans la base de données
    curseur.execute('DELETE FROM commentaire WHERE image = %s',(nom_image)) #Supprime les commentaires de l'image
    os.remove(img_path) #Supprime l'image dans le dossier
    curseur.close()
    connexion.close()
    return render_template('supprimer_validee.html')

@app.route('/envoie-message', methods= ['POST'])
def recupere_message():
    nom_image = request.form['nom_image']
    auteur = request.form['auteur']
    contenu = request.form['contenu']  
    connexion = mysql.connect()
    curseur = connexion.cursor()
    curseur.execute('INSERT INTO commentaire (contenu, auteur, image) VALUES (%s, %s, %s)', (contenu, auteur, nom_image))
    curseur.close()
    connexion.commit()
    connexion.close()
    return redirect(url_for('affiche_page_image', nom_image=nom_image))

@app.route('/supprimer-message', methods=['POST'])
def supprime_message():
    nom_image = request.args['nom_image']
    identifier = request.args['id']
    connexion = mysql.connect()
    curseur = connexion.cursor()
    curseur.execute('DELETE FROM commentaire WHERE id = %s', (identifier))
    connexion.commit()
    curseur.close()
    connexion.close()
    return redirect(url_for('affiche_page_image', nom_image = nom_image))

@app.route('/commentaire')
def affiche_commentaire():
    nom_image = request.args['nom_image']
    identifier = request.args['id']
    connexion = mysql.connect()
    curseur = connexion.cursor()
    curseur.execute('SELECT contenu, auteur, date_mise_en_ligne FROM commentaire WHERE id = %s', (identifier))
    commentaire = curseur.fetchone()
    curseur.close()
    connexion.close()
    if commentaire == None:
        return redirect(url_for('affiche_page_image'))
    else:
        return render_template('commentaire.html', commentaire = commentaire, id=identifier, nom_image = nom_image)

@app.route('/commentaire/formulaire')
def affiche_modification_commentaire():
    identifier = request.args['id']
    nom_image = request.args['nom_image']
    connexion = mysql.connect()
    curseur = connexion.cursor()
    curseur.execute('SELECT contenu, auteur, date_mise_en_ligne FROM commentaire WHERE id = %s', (identifier))
    commentaire = curseur.fetchone()
    curseur.close()
    connexion.close()
    if commentaire == None:
        return redirect(url_for('affiche_page_message'))
    else:
        return render_template('formulaire_commentaire.html',  commentaire = commentaire, id=identifier, nom_image = nom_image)

@app.route('/commentaire/modifie', methods=['POST'])
def modifie_message():
    identifier = request.args['id']
    nom_image = request.args['nom_image']
    connexion = mysql.connect()
    curseur = connexion.cursor()
    contenu = request.form['contenu']
    auteur = request.form['auteur']
    date_publication = datetime.strptime(request.form['date_publication'], '%d/%m/%Y %H:%M:%S')
    #Met à jour le commentaire dans la base de données
    curseur.execute('UPDATE commentaire SET contenu = %s, auteur = %s, date_mise_en_ligne = %s WHERE id = %s', (contenu, auteur, date_publication, identifier))
    curseur.close()
    connexion.commit()
    connexion.close()
    return redirect(url_for('affiche_page_image', id=identifier, nom_image = nom_image))

app.run(debug=True)
