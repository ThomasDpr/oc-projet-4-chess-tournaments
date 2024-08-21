# Gestion de Tournois d'Échecs

Bienvenue dans l'application de gestion de tournois d'échecs ! Cette application vous permet de gérer des joueurs, des tournois et de générer des rapports hors ligne de manière simple et efficace.

## Table des Matières

- [Prérequis](#prérequis)
- [Cloner le dépôt](#cloner-le-dépôt)
- [Installation des dépendances](#installation-des-dépendances)

  - [Recommandé : Pipenv](#recommandé--pipenv)
  - [Classique : Pip](#classique--pip)

- [Lancement du Programme](#lancement-du-programme)
- [Fonctionnalités](#fonctionnalités)

## Prérequis

- Python 3.11 ou supérieur
- Pip (Gestionnaire natif de Python)
- Pipenv (Gestionnaire de dépendances)

Ce projet a été conçu avec la version de Python `3.12.3` et le gestionnaire de dépendances **`Pipenv`** (version `2023.12.1`).

Je vous recommande l'utilisation de Pipenv pour gérer les dépendances de ce projet.

Si toutefois vous souhautez utiliser le gestionnaire de dépendances native de Python : `pip`, le fichier `requirements.txt` contient toutes les dépendances du projet et sera très utile pour vous. Rendez-vous à la section [Installation des dépendances avec Pip](#classique--pip) pour plus de détails.

## Cloner le dépôt

1. **Ouvrez votre terminal et clonez le dépôt :**

   ```sh
   git clone https://github.com/ThomasDpr/oc-projet-4-chess-tournaments.git
   ```

2. **Dirigez-vous dans le dossier du projet :**

   ```sh
   cd oc-projet-4-chess-tournaments
   ```

## Installation des dépendances

Choisissez le type d'installation que vous souhaitez (Pipenv ou Pip)

### Recommandé : Pipenv

1. **Si ce n'est pas déjà fait, installez Pipenv sur votre machine :**

   Si vous utilisez `python3`, remplacez `pip` par `pip3`.

   ```sh
   pip install pipenv
   ```

2. **Vérifiez que Pipenv est bien installé :**

   ```sh
   pipenv --version
   ```

   Vous devriez voir la version de Pipenv affichée:

   ```sh
   pipenv, version 2023.12.1
   ```

3. **Installez les dépendances du projet :**

   ```sh
   pipenv install
   ```

4. **Activez les dépendances du projet :**

   ```sh
   pipenv shell
   ```

### Classique : Pip

1. **Installez les dépendances du projet :**

   Si vous utilisez `python3`, remplacez `pip` par `pip3`.

   ```sh
   pip install -r requirements.txt
   ```

## Lancement du Programme

──────────[ ❗️ IMPORTANT ❗️ ]──────────

Avant de lancer le programme, il est **extrêmement recommandé** <u>d'étendre votre terminal au maxiumum</u> pour profiter pleinement de toutes les fonctionnalités offertes par le programme.

──────────[ ❗️ IMPORTANT ❗️ ]──────────

1. **Pour démarrer le programme**

   Si vous utilisez `python3`, remplacez `python` par `python3`.

   ```sh
   python main.py
   ```

## Fonctionnalités

### Gestion des joueurs

Dans ce menu, vous avez accès à cinq fonctionnalités :

- Ajouter un joueur
- Supprimer un joueur
- Rechercher un joueur
- Afficher tous les joueurs
- Retour au menu principal

Tout ajout ou suppression de joueur entraînera la modification immédiate du fichier `datas/players.json`.

### Gestion des tournois

Dans ce menu, vous avez accès à cinq fonctionnalités :

- Ajouter un tournoi
- Démarrer un tournoi
- Reprendre un tournoi
- Liste de tous les tournois
- Retour au menu principal

Tout ajout, lancement ou reprise de tournoi entraînera la modification immédiate du fichier `datas/tournaments.json`.

### Gestion des rapports

Dans ce menu, vous avez accès à six fonctionnalités :

- Liste de tous les joueurs (A-Z)
- Liste de tous les tournois
- Nom et dates d'un tournoi donné
- Liste des joeurs d'un tournoi (A-Z)
- Liste de tous les tours du tournoi et de tous les matchs du tour
- Retour au menu principal

Chacune de ces fonctionnalités permet degénérer des rapports visuels détaillés dans votre terminal.
Mais il est plus agréable de pouvoir en extraire les données dans ces trois formats :

- HTML
- TXT
- CSV

Pour cela, il vous suffit de sélectionner `Exporter` quand il vous sera demandé, puis de choisir le format d'exportation souhaité.

Tous les fichiers exportés seront stockés dans le dossier `reports`.
