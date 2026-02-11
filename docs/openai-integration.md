# Intégration OpenAI - EcoWatch Backend

Ce document détaille l'architecture et la maintenance du service OpenAI intégré dans le backend EcoWatch.

## Architecture

Le service est divisé en modules spécialisés dans `monitoring/services/openai/` :

- **`config.py`** : Paramètres des modèles et constantes de coût.
- **`client.py`** : Gestionnaire de requêtes HTTP brut (timeout, headers).
- **`error_handler.py`** : Logique de retry et traduction des codes d'erreur.
- **`logger.py`** : Monitoring de la consommation (tokens) et des performances.
- **`service.py`** : Interface métier principale.

## Maintenance et Sécurité

### Mise à jour de la clé API
La clé est stockée dans le fichier `.env` sous la variable `OPENAI_API_KEY`. 
Le serveur redémarre automatiquement lors d'une modification de ce fichier sous Django.

### Changement de modèle
Pour passer de GPT-3.5 à GPT-4, modifiez la valeur `primary` dans `config.py`.

### Monitoring des coûts
Consultez les logs du serveur (Django console). Chaque appel est loggué avec :
- Le nombre de tokens (Input/Output)
- Une estimation du coût en USD
- La latence de la requête

## Gestion des Erreurs

Le système implémente un **Backoff Exponentiel**. Si l'API OpenAI est surchargée ou rencontre une erreur réseau, elle réessaiera automatiquement 3 fois avant de renvoyer une erreur finale.

### Codes d'erreurs communs
- **429 (Quota)** : Le message indique si c'est une limite de débit ou un manque de fonds sur le compte.
- **401 (Auth)** : Vérifiez la clé dans le fichier `.env`.
- **500/503** : Erreur côté OpenAI, le système réessaiera automatiquement.

## Test Rapide
Pour vérifier l'intégration, utilisez le Chatbot EcoWatch. Si Gemini est désactivé (via `FORCE_OPENAI=True` dans `ai_service.py`), tous les appels passeront par ce nouveau service.
