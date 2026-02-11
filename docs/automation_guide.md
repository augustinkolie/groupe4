# Guide d'Automatisation et Ingestion

Ce guide référence les commandes nécessaires pour gérer l'ingestion des données de qualité de l'air et l'automatisation via Django Q.

## 1. 📥 Ingestion Manuelle

Pour déclencher immédiatement la récupération des données depuis OpenWeather et leur insertion en base :

```bash
python manage.py fetch_air_quality
```
*Cette commande récupère les données pour toutes les stations virtuelles, calcule l'IQA et sauvegarde les relevés.*

## 2. 🕒 Configuration de la Planification

Le système est configuré pour lancer l'ingestion automatiquement **toutes les 10 minutes**.

Pour vérifier ou réinitialiser cette planification, exécutez le script :
```bash
python schedule_ingestion.py
```
*Ce script interagit avec la base de données de `Django Q` pour s'assurer que la tâche `fetch_air_quality_task` est bien programmée.*

## 3. ⚙️ Exécution des Tâches (Cluster)

Pour que les tâches planifiées s'exécutent réellement, un processus "worker" doit tourner en permanence.
Dans un terminal dédié, lancez :

```bash
python manage.py qcluster
```

> **Note :** Si ce processus n'est pas lancé, les tâches seront mises en file d'attente mais ne seront jamais traitées.

## 4. 🔑 Rotation des Clés Gemini

Le système gère automatiquement la rotation des clés API Gemini en cas de dépassement de quota.
Assurez-vous que votre fichier `.env` contient bien les clés secondaires :

```env
GOOGLE_GENAI_API_KEY=principale
GOOGLE_GENAI_API_KEY_2=secours_1
GOOGLE_GENAI_API_KEY_3=secours_2
```
