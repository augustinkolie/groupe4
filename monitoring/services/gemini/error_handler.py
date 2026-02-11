import logging
import time

logger = logging.getLogger(__name__)

class GeminiError(Exception):
    """Exception de base pour les erreurs du service Gemini."""
    def __init__(self, message, error_code=None, safety_ratings=None):
        super().__init__(message)
        self.error_code = error_code
        self.safety_ratings = safety_ratings

def handle_gemini_response_error(response):
    """Gère les erreurs dans la réponse Gemini (ex: contenu bloqué)."""
    try:
        # Vérification si la réponse a été bloquée par les filtres de sécurité
        if hasattr(response, 'candidates') and not response.candidates:
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                reason = response.prompt_feedback.block_reason
                return GeminiError(f"Contenu bloqué par les filtres de sécurité Google (Raison: {reason})", "safety_block")
            return GeminiError("Réponse vide de Gemini (possible blocage de sécurité).", "empty_response")
    except Exception as e:
        return GeminiError(f"Erreur lors de l'analyse de la réponse : {str(e)}", "parse_error")
    
    return None

def execute_with_retry(func, *args, **kwargs):
    """Système de retry simple pour les erreurs réseau ou 429."""
    from .config import MAX_RETRIES, INITIAL_BACKOFF
    retries = 0
    backoff = INITIAL_BACKOFF
    
    while retries < MAX_RETRIES:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            retries += 1
            error_msg = str(e)
            
            # Si c'est une erreur de quota (429) ou de serveur (500/503), on réessaie
            if "429" in error_msg or "500" in error_msg or "503" in error_msg or "quota" in error_msg.lower():
                if retries >= MAX_RETRIES:
                    raise GeminiError(f"Quota Gemini épuisé ou service indisponible après {MAX_RETRIES} tentatives.", "api_failure")
                
                logger.warning(f"Gemini API Error (Tentative {retries}/{MAX_RETRIES}). Backoff {backoff}s...")
                time.sleep(backoff)
                backoff *= 2
            else:
                # Autres erreurs (auth, etc.), on ne réessaie pas forcément
                raise GeminiError(f"Erreur API Gemini : {error_msg}", "api_error")
