import time
import logging
import requests
from .config import MAX_RETRIES, INITIAL_BACKOFF

logger = logging.getLogger(__name__)

class OpenAIError(Exception):
    """Exception de base pour les erreurs du service OpenAI."""
    def __init__(self, message, status_code=None, details=None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details

def handle_api_error(response):
    """Analyse les codes d'erreur HTTP et lève des exceptions explicites."""
    status_code = response.status_code
    try:
        error_data = response.json().get('error', {})
        error_msg = error_data.get('message', 'Erreur inconnue')
        error_code = error_data.get('code', 'unknown_error')
    except:
        error_msg = response.text
        error_code = "parse_error"

    if status_code == 401:
        return OpenAIError("Clé API invalide ou expirée.", status_code, error_msg)
    elif status_code == 429:
        if "insufficient_quota" in error_msg or "billing" in error_msg:
            return OpenAIError("Quota épuisé ou solde insuffisant sur le compte OpenAI.", status_code, error_msg)
        return OpenAIError("Limite de débit atteinte (Rate limited).", status_code, error_msg)
    elif status_code >= 500:
        return OpenAIError("Le service OpenAI rencontre des problèmes temporaires.", status_code, error_msg)
    
    return OpenAIError(f"Erreur API ({status_code}): {error_msg}", status_code, error_msg)

def execute_with_retry(func, *args, **kwargs):
    """Exécute une fonction avec un système de retry simple (backoff exponentiel)."""
    retries = 0
    backoff = INITIAL_BACKOFF
    
    while retries < MAX_RETRIES:
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                raise OpenAIError(f"Échec après {MAX_RETRIES} tentatives : {str(e)}")
            
            logger.warning(f"Tentative {retries} échouée. Nouvelle tentative dans {backoff}s...")
            time.sleep(backoff)
            backoff *= 2 # Backoff exponentiel
