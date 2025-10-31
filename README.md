# API de Prédiction de Risque Cardiaque (Cardio Risk API)

Cette API, développée avec FastAPI, utilise un modèle de Machine Learning (***Random Forest***) pour prédire le risque de maladie cardiaque (positif/négatif) en se basant sur les données d'un patient.

Elle fournit également des points de terminaison (***endpoints***) pour gérer une base de données de patients via des opérations CRUD (***Create***, ***Read***).

## Technologies Utilisées

  * ***Backend*** : FastAPI, Uvicorn

  * ***Base de Données*** : SQLite (via SQLAlchemy)

  * ***Validation de Données*** : Pydantic

  * ***Machine Learning*** : Scikit-learn (*RandomForestClassifier*, *SelectKBest*, *Pipeline*), Pandas

  * ***Sérialisation du Modèle*** : Joblib

## Installation et Lancement

### Cloner le dépôt

git clone [URL_DE_VOTRE_DEPOT]
cd [NOM_DU_DOSSIER]


### Créer un environnement virtuel

python -m venv venv
**Sur Windows:** venv\Scripts\activate


### Installer les dépendances
(Créez un fichier requirements.txt avec le contenu ci-dessous, puis exécutez ***pip install -r requirements.txt***)

### contenu de requirements.txt:

  * fastapi
  * uvicorn[standard]
  * sqlalchemy
  * pydantic
  * joblib
  * pandas
  * numpy
  * scikit-learn


### Démarrer l'API
L'API (***main.py***) s'attend à trouver le modèle dans un dossier ***Model/.*** Assurez-vous de placer ***joblib.dump*** dans ***Model/joblib.dump*** ou de modifier le chemin dans main.py.

***uvicorn main:app --reload***


### Accéder à l'API

***API :*** http://127.0.0.1:8000

***Documentation (Swagger) :*** http://127.0.0.1:8000/docs

## À Propos du Modèle de Machine Learning

Le modèle (défini dans ***NoteBook.ipynb*** et sauvegardé dans ***joblib.dump***) est un Pipeline Scikit-learn qui effectue deux étapes :

### Sélection de Caractéristiques (Features)

Utilise SelectKBest ***(avec f_classif, k=4)*** pour sélectionner les 4 caractéristiques les plus prédictives.

D'après le notebook, les caractéristiques sélectionnées sont : ***age, gender, kcm, troponin.***

### Modèle de Classification

Un RandomForestClassifier est utilisé pour la prédiction binaire (positif/négatif).

### Performance du Modèle

(Basée sur l'ensemble de test du Notebook)

***Accuracy*** : 0.981

***F1-Score*** : 0.984

## Structure de la Base de Données

L'API utilise une base de données SQLite (***patients.db***) avec une table : patients.

Schéma de la table patients :

***id*** (Integer, Primary Key)

***name*** (String)

***age*** (Integer)

***gender*** (Integer)

***pressurehight*** (Integer)

***pressurelow*** (Integer)

***glucose*** (Integer)

***kcm*** (Integer)

***troponin*** (Integer)

***impluse*** (Integer)

## Endpoints de l'API

Consultez la documentation interactive sur ***http://127.0.0.1:8000/docs*** pour tester les endpoints.

#### GET /

Description : Message de bienvenue de l'API.

Réponse :

***{ "message": "bienvenue sur mon API" }***


#### POST /patients/

Description : Ajoute un nouveau patient à la base de données.

Corps (Body) attendu :

{
  ***"name":*** "John Doe",
  ***"age":*** 60,
  ***"gender":*** 1.0,
  ***"pressurehight":*** 98.0,
  ***"pressurelow":*** 46.0,
  ***"glucose":*** 296.0,
  ***"kcm":*** 1.75,
  ***"troponin":*** 0.06,
  ***"impluse":*** 94.0
}


Réponse : L'objet patient créé (incluant son ***id***).

#### GET /patients/

Description : Récupère la liste de tous les patients enregistrés dans la base de données.

Réponse : Une liste d'objets ***PatientResponse***.

#### GET /patients/{P_id}

Description : Récupère un patient spécifique par son ***id***.

Réponse : Un objet ***PatientResponse.***

#### GET /patients/Pred_risk/{P_id}

Description : Prédit le risque cardiaque (positif/négatif) pour un patient spécifique identifié par son P_id dans la base de données.

Réponse : Note : Le code actuel dans main.py retourne les données du patient (***PatientGet***) et non la prédiction. Le modèle s'attend à recevoir un DataFrame pandas pour la prédiction.
