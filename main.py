import requests
import sqlite3
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv('OPENWEATHER_API_KEY')


if not API_KEY:
    print("ERREUR: La clé API n'est pas définie dans le fichier .env")
    exit()


URL_API = "https://api.openweathermap.org/data/2.5/weather"
NOM_BASE_DONNEES = "weather_data.db"


villes = ['Dakar','Libreville', 'Paris', 'New York', 'Tokyo', 'London']

print("=" * 50)
print("DÉBUT DU PIPELINE ETL")
print("=" * 50)

# ====================================
# ÉTAPE 1 : EXTRACTION (Extract)
# ====================================
print("\n[1/3] EXTRACTION des données...")

donnees_meteo = []

for ville in villes:
    
    parametres = {
        'q': ville,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'fr'
    }
    
    
    reponse = requests.get(URL_API, params=parametres)
    data = reponse.json()
    
    
    enregistrement = {
        'ville': data['name'],
        'pays': data['sys']['country'],
        'temperature': data['main']['temp'],
        'ressenti': data['main']['feels_like'],
        'humidite': data['main']['humidity'],
        'pression': data['main']['pressure'],
        'vitesse_vent': data['wind']['speed'],
        'description': data['weather'][0]['description'],
        'visibilite': data.get('visibility', 0),
        'lever_soleil': data['sys']['sunrise'],
        'coucher_soleil': data['sys']['sunset']
    }
    
    donnees_meteo.append(enregistrement)
    print(f"Données extraites pour {ville}")


df = pd.DataFrame(donnees_meteo)

print(f"\n {len(df)} enregistrements extraits")

# ====================================
# ÉTAPE 2 : TRANSFORMATION (Transform)
# ====================================
print("\n[2/3] TRANSFORMATION des données...")

# Transformation 1: Convertir les timestamps en dates lisibles
df['lever_soleil_dt'] = pd.to_datetime(df['lever_soleil'], unit='s')
df['coucher_soleil_dt'] = pd.to_datetime(df['coucher_soleil'], unit='s')
print("1. Conversion des timestamps")

# Transformation 2: Calculer la durée du jour
df['duree_jour_heures'] = ((df['coucher_soleil'] - df['lever_soleil']) / 3600).round(2)
print("2. Calcul de la durée du jour")

# Transformation 3: Catégorie de température
def categorie_temp(temp):
    if temp < 0:
        return 'Très froid'
    elif temp < 10:
        return 'Froid'
    elif temp < 20:
        return 'Frais'
    elif temp < 30:
        return 'Agréable'
    else:
        return 'Chaud'

df['categorie_temp'] = df['temperature'].apply(categorie_temp)
print("3. Catégorisation des températures")

# Transformation 4: Indice de confort
df['indice_confort'] = (df['temperature'] - (df['humidite'] / 10)).round(2)
print("4. Calcul de l'indice de confort")

# Transformation 5: Convertir visibilité en km
df['visibilite_km'] = (df['visibilite'] / 1000).round(2)
print("5. Conversion visibilité en km")

# Transformation 7: Ajouter la date d'extraction
df['date_extraction'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("6. Ajout de la date d'extraction")





# ====================================
# ÉTAPE 3 : CHARGEMENT (Load)
# ====================================
print("\n[3/3] CHARGEMENT dans la base de données...")

# Connexion à la base SQLite
connexion = sqlite3.connect(NOM_BASE_DONNEES)

# Insérer les données dans la table
df.to_sql('meteo', connexion, if_exists='replace', index=False)

# Vérifier le chargement
curseur = connexion.cursor()
curseur.execute("SELECT COUNT(*) FROM meteo")
nombre = curseur.fetchone()[0]

print(f" {nombre} enregistrements chargés dans '{NOM_BASE_DONNEES}'")

# Afficher un aperçu
print("\n=== Aperçu des données ===")
apercu = pd.read_sql_query("SELECT ville, temperature, categorie_temp, humidite FROM meteo", connexion)
print(apercu.to_string())


connexion.close()

print("\n" + "=" * 50)
print("PIPELINE ETL TERMINÉ AVEC SUCCÈS !")
print("=" * 50)