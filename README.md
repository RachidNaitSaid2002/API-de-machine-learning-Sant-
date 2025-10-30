# API-de-machine-learning-Sant-
# Documentation Brief N°4

**Délai :** 27 Octobre 2025 - 31 Octobre 2025

---

## Tâches Backend

### 1. [Backend] Configurer l'environnement Git Backend
- [ ] Cloner le dépôt du projet en utilisant l'URL SSH.
- [ ] Créer une branche locale nommée `feat/backend` à partir de `main`.
- [ ] Publier (pousser) la branche `feat/backend` sur le dépôt distant (GitHub/GitLab).

### 2. [Backend] Mettre en place la Base de Données (SQLite)
- [ ] Configurer le moteur de base de données SQLite dans FastAPI (ex: avec `SQLAlchemy` ou `SQLModel`).
- [ ] Définir le modèle de données (schéma) pour un `Patient` en base (ex: `PatientInDB`).
- [ ] S'assurer que l'API crée le fichier de base de données au démarrage.

> **Note :** Cette tâche est cruciale avant de créer les endpoints.

### 3. [Backend] Créer l'endpoint Create (`POST /patients`)
- [ ] Implémenter la route `POST /patients`.
- [ ] La route doit prendre les données du patient (format `PatientInput`).
- [ ] La route doit sauvegarder le patient dans la base de données SQLite et retourner le patient créé (format `PatientInDB`).

### 4. [Backend] Créer l'endpoint Read (`GET /patients`)
- [ ] Implémenter la route `GET /patients/{patient_id}` pour lire un patient.
-