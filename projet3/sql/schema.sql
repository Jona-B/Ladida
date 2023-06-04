-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : Dim 10 jan. 2021 à 01:48
-- Version du serveur :  8.0.21
-- Version de PHP : 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `projet3`
--
DROP DATABASE IF EXISTS projet3;
CREATE DATABASE `projet3` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `projet3`;

-- --------------------------------------------------------

--
-- Structure de la table `commentaire`
--

DROP TABLE IF EXISTS `commentaire`;
CREATE TABLE IF NOT EXISTS `commentaire` (
  `id` int NOT NULL AUTO_INCREMENT,
  `contenu` text NOT NULL,
  `date_mise_en_ligne` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `image` varchar(200) NOT NULL,
  `auteur` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Déchargement des données de la table `commentaire`
--

INSERT INTO `commentaire` (`id`, `contenu`, `date_mise_en_ligne`, `image`, `auteur`) VALUES
(2, 'Are you ready ? Let\'s go !', '2021-01-10 02:41:17', 'love4eva.gif', 'Alexandre'),
(3, 'Dans la jungle, terrible jungle\r\nLe lion est mort ce soir\r\nEt les hommes tranquilles s\'endorment\r\nLe lion est mort ce soir\r\nA-wimboé, a-wimboé, a-wimboé, a-wimboé\r\nA-wimboé, a-wimboé, a-wimboé\r\nA-wimboé, a-wimboé, a-wimboé, a-wimboé\r\nA-wimboé, a-wimboé, a-wimboé', '2021-01-10 02:41:32', 'Jungle_Plan_de_travail_1.jpg', 'Alexandre'),
(4, 'Please vote Yellow suspect', '2021-01-10 02:41:57', 'yellownoel.png', 'Alexandre'),
(5, 'Yellow was the Imposter', '2021-01-10 02:42:07', 'yellownoel.png', 'Alexandre'),
(6, 'LA-LA-LA-LA', '2021-01-10 02:42:23', 'Everglow_adios.mp4', 'Alexandre'),
(7, 'ding dong', '2021-01-10 02:42:37', 'drum-hitfinish.mp3', 'Alexandre');

-- --------------------------------------------------------

--
-- Structure de la table `image`
--

DROP TABLE IF EXISTS `image`;
CREATE TABLE IF NOT EXISTS `image` (
  `nom` varchar(250) NOT NULL,
  `createur` varchar(100) NOT NULL,
  `titre` varchar(100) NOT NULL,
  `date_mise_en_ligne` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type_fichier` varchar(255) NOT NULL,
  PRIMARY KEY (`nom`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Déchargement des données de la table `image`
--

INSERT INTO `image` (`nom`, `createur`, `titre`, `date_mise_en_ligne`, `type_fichier`) VALUES
('city00.jpg', 'Alexandre', 'Ville', '2021-01-10 02:39:04', 'image'),
('Jungle_Plan_de_travail_1.jpg', 'Alexandre', 'Jungle', '2021-01-10 02:39:12', 'image'),
('love4eva.gif', 'Alexandre', 'A gauche puis à droite !', '2021-01-10 02:39:20', 'image'),
('Menu_Plan_de_travail_1.jpg', 'Alexandre', '6 Weeks Project', '2021-01-10 02:39:28', 'image'),
('yellownoel.png', 'Alexandre', 'Yellow Xmas', '2021-01-10 02:39:37', 'image'),
('RH_BIG_DATA_1.jpg', 'Alexandre', 'BigDATA', '2021-01-10 02:39:58', 'image'),
('drum-hitfinish.mp3', 'Alexandre', 'Bell Sound', '2021-01-10 02:40:26', 'audio'),
('Everglow_adios.mp4', 'Alexandre', 'Adios Everglow', '2021-01-10 02:40:38', 'video'),
('flan.mp4', 'Alexandre', 'Flan', '2021-01-10 02:40:51', 'video'),
('lalala.mp3', 'Alexandre', 'La La La', '2021-01-10 02:47:06', 'audio');

-- --------------------------------------------------------

--
-- Structure de la table `membre`
--

DROP TABLE IF EXISTS `membre`;
CREATE TABLE IF NOT EXISTS `membre` (
  `pseudonyme` varchar(100) NOT NULL,
  `mot_de_passe_chiffre` varchar(255) NOT NULL,
  PRIMARY KEY (`pseudonyme`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Déchargement des données de la table `membre`
--

INSERT INTO `membre` (`pseudonyme`, `mot_de_passe_chiffre`) VALUES
('Alexandre', 'pbkdf2:sha256:150000$To1lA3GU$ffedc83cb452af74cf680eddf8086faa7ede539f08444e672c412c4a8148d8f5');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
