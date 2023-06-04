DROP DATABASE IF EXISTS projet3;
CREATE DATABASE projet3;
USE projet3;
CREATE TABLE membre (
  pseudonyme varchar(100) NOT NULL,
  mot_de_passe_chiffre varchar(255) NOT NULL,
  PRIMARY KEY (pseudonyme)
);

USE projet3;
CREATE TABLE image (
  nom varchar(250) NOT NULL,
  createur varchar(100) NOT NULL,
  titre varchar(100) NOT NULL,
  date_mise_en_ligne datetime NOT NULL DEFAULT NOW(),
  type_fichier varchar(255) NOT NULL,
  PRIMARY KEY (nom)
);

USE projet3;
CREATE TABLE commentaire(
  id int NOT NULL AUTO_INCREMENT,
  contenu TEXT NOT NULL,
  date_mise_en_ligne DATETIME NOT NULL DEFAULT NOW(),
  image VARCHAR(200) NOT NULL,
  auteur VARCHAR(100) NOT NULL,
  PRIMARY KEY (id)
);