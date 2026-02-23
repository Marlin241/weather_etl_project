#  Projet ETL - OpenWeatherMap

Projet de Data Engineering pour extraire, transformer et charger des données météorologiques depuis l'API OpenWeatherMap.

## Objectifs du projet

-  Créer un projet structuré
-  Utiliser un environnement virtuel Python
-  Extraire des données depuis OpenWeatherMap (min. 7 variables)
-  Effectuer des transformations de données (min. 5 transformations)
-  Charger les données dans une base SQLite
-  Gérer les secrets avec des variables d'environnement

##  Structure du projet

```
weather_etl_project/
├── main.py          # Script principal ETL
├── .env.example           # Template pour les variables d'environnement
├── .gitignore            # Fichiers à ignorer par Git
├── README.md             # Ce fichier
└── weather_data.db       # Base de données SQLite (généré après exécution)
```

##  Installation

### 1. Prérequis

- Python 3.8 ou supérieur
- pip ou uv
- Compte OpenWeatherMap (gratuit)

### 2. Obtenir une clé API

1. Créer un compte sur [OpenWeatherMap](https://openweathermap.org/)
2. Aller dans **API Keys** dans votre profil
3. Copier votre clé API

### 3. Configuration de l'environnement





```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
```

### 4. Configurer la clé API

Éditer le fichier `.env` et ajouter votre clé API:

```bash
OPENWEATHER_API_KEY=votre_cle_api_ici
```

## Variables extraites (11 au total)

Le script extrait les variables suivantes depuis l'API:

1. **ville** - Nom de la ville
2. **pays** - Code du pays
3. **temperature** - Température en °C
4. **ressenti** - Température ressentie en °C
5. **humidite** - Humidité en %
6. **pression** - Pression atmosphérique en hPa
7. **vitesse_vent** - Vitesse du vent en m/s
8. **description** - Description météo
9. **visibilite** - Visibilité en mètres
10. **lever_soleil** - Heure de lever du soleil (timestamp)
11. **coucher_soleil** - Heure de coucher du soleil (timestamp)

##  Transformations effectuées (7 au total)

1. **Conversion timestamps** - Transformation des timestamps Unix en datetime lisibles
2. **Calcul durée du jour** - Calcul de la durée d'ensoleillement en heures
3. **Catégorisation température** - Classification: Très froid, Froid, Frais, Agréable, Chaud
4. **Indice de confort** - Calcul d'un indice basé sur température et humidité
5. **Conversion visibilité** - Conversion de mètres en kilomètres
6. **Normalisation descriptions** - Mise en forme des descriptions météo
7. **Identifiants uniques** - Ajout d'ID pour chaque enregistrement

##  Base de données

Les données sont stockées dans une base SQLite (`weather_data.db`) avec la table:

- **meteo** - Qui contient toutes les métriques météorologiques transformées

##  Exécution

```bash

# Exécuter le pipeline ETL
python main.py
```

##  Exemple de sortie

```
============================================================
PIPELINE ETL - OpenWeatherMap
============================================================

[1/3] EXTRACTION des données...
 Données extraites pour Dakar
 Données extraites pour Libreville
 Données extraites pour New York
...

[2/3] TRANSFORMATION de 7 enregistrement(s)...
=== Transformations des données ===
1. Conversion timestamps Unix → datetime
2. Calcul de la durée du jour
3. Catégorisation de la température
4. Calcul de l'indice de confort
5. Conversion visibilité (m → km)
6. Normalisation des descriptions météo
7. Ajout d'identifiants uniques

[3/3] CHARGEMENT dans la base de données...
 7 enregistrement(s) chargé(s) dans la base de données

============================================================
Pipeline ETL terminé avec succès !
============================================================
```

##  Interroger la base de données

```bash
# Ouvrir la base de données
sqlite3 weather_data.db

# Exemples de requêtes SQL
SELECT * FROM meteo;
SELECT * FROM meteo WHERE temperature > 25;
```

##  Technologies utilisées

- **Python 3** - Langage de programmation
- **requests** - Requêtes HTTP vers l'API
- **pandas** - Manipulation et transformation des données
- **sqlite3** - Base de données relationnelle
- **python-dotenv** - Gestion des variables d'environnement

##  Sécurité

-  Clé API stockée dans variable d'environnement
-  Fichier `.env` exclu du contrôle de version (.gitignore)
-  Template `.env.example` fourni pour la documentation

##  Bonnes pratiques appliquées

-  Code documenté avec docstrings
-  Séparation Extract-Transform-Load (ETL)
-  Gestion des erreurs
-  Messages de log informatifs
-  Structure de projet organisée
-  Environnement virtuel isolé
-  Gestion sécurisée des secrets

##  Contribution

Projet académique de Data Engineering.

##  Licence

Projet éducatif - 2026

---
*Développé par Marlin241 pour le cours de Data Engineering, github : https://github.com/Marlin241*
