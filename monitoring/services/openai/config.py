import os

# Paramètres des modèles OpenAI
OPENAI_MODELS = {
    "primary": "gpt-3.5-turbo",
    "advanced": "gpt-4-turbo",
}

# Paramètres par défaut des requêtes
DEFAULT_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "timeout": 30, # secondes
}

# Coûts estimés (par 1k tokens) - GPT-3.5-Turbo (ordre de grandeur)
COST_PER_1K_TOKENS = {
    "input": 0.0005,
    "output": 0.0015,
}

# Configuration du Retry
MAX_RETRIES = 3
INITIAL_BACKOFF = 1 # seconde
