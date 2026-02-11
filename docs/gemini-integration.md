# Intégration Google Gemini - EcoWatch Backend

Ce document détaille l'architecture et la maintenance du service Google Gemini intégré dans le backend EcoWatch.

## Architecture

Le service est divisé en modules spécialisés dans `monitoring/services/gemini/` :

- **`config.py`** : Modèles (Gemini 2.0 Flash) et paramètres de génération.
- **`safety_config.py`** : Configuration des filtres de sécurité Google.
- **`client.py`** : Initialisation du SDK `google-generativeai`.
- **`error_handler.py`** : Gestion des blocages de sécurité et retries réseau.
- **`logger.py`** : Suivi des tokens, des coûts et des safety ratings.

## Maintenance et Sécurité

### Mise à jour de la clé API
La clé est stockée dans le fichier `.env` sous `GOOGLE_GENAI_API_KEY`.

### Sécurité et Contenu bloqué
Gemini possède des filtres de sécurité stricts. Si une réponse est bloquée, le `error_handler.py` lèvera une exception explicite et le système basculera automatiquement sur OpenAI (moins restrictif).

### Support Multimodal
Le `GeminiService` est prêt pour le multimodal. Pour analyser une image :
```python
service.generate_content("Décris cette image", images=[image_data])
```

## Monitoring

Les appels Gemini sont loggués dans la console Django avec :
- Le nombre de tokens consommés.
- Les éventuels "Safety Ratings" si le contenu est sensible.
- Le temps de réponse.

## Dépannage
- **Erreur 429** : Limite de quota gratuit atteinte. Le système attendra et réessaiera, ou passera sur OpenAI.
- **Réponse vide** : Souvent dû à un blocage de sécurité. Vérifiez les `safety_settings.py`.
