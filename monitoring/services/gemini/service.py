import time
import logging
from .client import GeminiClient
from .config import GEMINI_MODELS
from .logger import log_gemini_call
from .error_handler import handle_gemini_response_error, execute_with_retry, GeminiError

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.client = GeminiClient()

    def generate_content(self, prompt, model_name=None, images=None):
        """Génère du contenu (texte ou multimodal)."""
        model_name = model_name or GEMINI_MODELS["primary"]
        model = self.client.get_model(model_name)
        
        start_time = time.time()
        try:
            # Construction du contenu (multimodal si images fournies)
            content = [prompt]
            if images:
                content.extend(images)

            # Exécution avec retry et rotation de clé
            response = execute_with_retry(
                model.generate_content, 
                content, 
                key_manager=self.client.key_manager
            )
            
            # Vérification des erreurs de sécurité/réponse
            error = handle_gemini_response_error(response)
            if error:
                raise error

            duration = time.time() - start_time
            
            # Extraction des métriques
            # Note: Le SDK Python peut ne pas renvoyer les tokens sur tous les modèles
            input_tokens = getattr(response.usage_metadata, 'prompt_token_count', 0)
            output_tokens = getattr(response.usage_metadata, 'candidates_token_count', 0)
            
            log_gemini_call(model_name, input_tokens, output_tokens, duration)
            return response.text

        except Exception as e:
            duration = time.time() - start_time
            log_gemini_call(model_name, 0, 0, duration, status=f"ERROR: {str(e)}")
            raise e
            
    def get_chat_response(self, user_message, context="", history=None):
        """Interface spécialisée pour le Chatbot avec mémoire."""
        
        # Construction de l'historique
        history_str = ""
        if history:
            history_str = "HISTORIQUE DE CONVERSATION (MÉMOIRE):\n"
            for msg in history:
                role = "Utilisateur" if msg.get("role") == "user" else "Assistant"
                history_str += f"- {role}: {msg.get('content')}\n"
            history_str += "\n"

        prompt = f"""
{history_str}
CONTEXTE ACTUEL (Données & Tendances):
{context}

NOUVELLE QUESTION UTILISATEUR:
{user_message}

CONSIGNE: Utilise l'historique pour comprendre le contexte (ex: "Et à Labé ?" se réfère à la question précédente). Réponds de manière concise.
"""
        return self.generate_content(prompt)
