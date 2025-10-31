# Pipeline d'Apprentissage Automatique pour la Prédiction du Statut Patient

Ce dépôt contient un Notebook Jupyter (`NoteBook.ipynb`) qui implémente un pipeline complet d'apprentissage automatique pour prédire le statut d'un patient (`positive` ou `negative`) basé sur divers indicateurs de santé.

Le notebook couvre le chargement des données, l'exploration initiale, l'ingénierie des fonctionnalités, l'entraînement du modèle, l'évaluation et la persistance du modèle.

## 📁 Structure du Projet

Les fichiers principaux de ce projet sont :

| Fichier | Description |
| :--- | :--- |
| `NoteBook.ipynb` | Le Notebook Jupyter principal contenant le flux de travail complet d'apprentissage automatique. |
| `data-68fe0fb66c2ee565848417.csv` | Le jeu de données utilisé pour l'entraînement et l'évaluation (nécessaire pour exécuter le notebook). |
| `joblib.dump` | Le modèle d'apprentissage automatique entraîné, sauvegardé à l'aide de `joblib` pour une utilisation ultérieure. |

## 📊 Données

Le jeu de données contient les fonctionnalités suivantes, qui semblent être liées à la santé du patient :

| Nom de la Colonne | Type de Données | Description |
| :--- | :--- | :--- |
| `age` | Entier | Âge du patient. |
| `gender` | Entier | Sexe du patient (probablement encodé en 0 et 1). |
| `pressurehight` | Entier | Lecture de la pression artérielle élevée (systolique). |
| `pressurelow` | Entier | Lecture de la pression artérielle basse (diastolique). |
| `glucose` | Flottant | Niveau de glucose. |
| `kcm` | Flottant | Niveau de KCM (probablement un marqueur cardiaque). |
| `troponin` | Flottant | Niveau de troponine (un marqueur cardiaque clé). |
| `impluse` | Entier | Pouls/Fréquence cardiaque. |
| **`status`** | Objet (Cible) | La variable cible à prédire (`positive` ou `negative`). |

## 🛠️ Méthodologie

Le flux de travail d'apprentissage automatique mis en œuvre dans le notebook suit ces étapes :

1.  **Chargement et Nettoyage des Données :** Les données sont chargées à partir de `data-68fe0fb66c2ee565848417.csv`. Le notebook inclut des vérifications des lignes en double et des valeurs manquantes.
2.  **Analyse Exploratoire des Données (AED) :** Le notebook comprend des visualisations (par exemple, des CountPlots pour `gender` et `status`) pour comprendre la distribution des données.
3.  **Ingénierie des Fonctionnalités :** La variable cible catégorielle (`status`) est convertie en un format numérique (`0` et `1`).
4.  **Entraînement du Modèle :** Un **Classifieur Forêt Aléatoire** (Random Forest Classifier) est entraîné à l'aide d'un `Pipeline` qui intègre la **Sélection de Fonctionnalités** (`SelectKBest` avec `f_classif`).
5.  **Évaluation :** La performance du modèle est évaluée à l'aide de l'**Exactitude** (Accuracy) et du **Score F1**.
    *   **Exactitude Observée :** ~0.981
    *   **Score F1 Observé :** ~0.985
6.  **Persistance du Modèle :** Le modèle `Pipeline` final entraîné est sauvegardé sur disque sous le nom `joblib.dump` à l'aide de la bibliothèque `joblib`.

## 🚀 Comment Exécuter le Notebook

### Prérequis

Vous devez avoir Python et les bibliothèques suivantes installées :

*   `pandas`
*   `matplotlib`
*   `seaborn`
*   `scikit-learn`
*   `joblib`
*   `jupyter` (pour exécuter le notebook)

Vous pouvez installer les bibliothèques requises en utilisant `pip` :

```bash
pip install pandas matplotlib seaborn scikit-learn joblib jupyter
```

### Exécution

1.  Assurez-vous que le fichier `data-68fe0fb66c2ee565848417.csv` se trouve dans le même répertoire que le `NoteBook.ipynb`. (Note : Ce fichier n'a pas été fourni, vous devrez donc le fournir pour exécuter le notebook avec succès).
2.  Ouvrez le Notebook Jupyter :
    ```bash
    jupyter notebook NoteBook.ipynb
    ```
3.  Exécutez toutes les cellules du notebook séquentiellement.

Les dernières cellules entraîneront le modèle, évalueront ses performances et sauvegarderont le modèle sous le nom `joblib.dump`. Le notebook inclut également un cas de test pour démontrer le chargement du modèle sauvegardé et la réalisation d'une prédiction pour un seul patient.

