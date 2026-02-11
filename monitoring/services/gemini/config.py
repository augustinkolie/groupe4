import os

# Modèles Gemini recommandés pour ce projet
GEMINI_MODELS = {
    "primary": "gemini-flash-latest", # Point vers la version Flash la plus stable
    "pro": "gemini-pro-latest",     # Point vers la version Pro la plus stable
}

# Paramètres par défaut des requêtes
DEFAULT_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
    "timeout": 60, # secondes
}

# Coûts estimés (par 1M tokens) - Ordre de grandeur Gemini 1.5 Flash
# Note: Gemini est souvent gratuit sous certains seuils
COST_PER_1M_TOKENS = {
    "input": 0.075,
    "output": 0.30,
}

# Configuration du Retry
MAX_RETRIES = 3
INITIAL_BACKOFF = 1 # seconde
