import time
from .client import OpenAIClient
from .config import OPENAI_MODELS, DEFAULT_CONFIG
from .logger import log_openai_call
from .error_handler import execute_with_retry

# Note: Correction du nom dans config si nécessaire, ici on utilise config directement
from . import config

class OpenAIService:
    def __init__(self):
        self.client = OpenAIClient()

    def get_chat_completion(self, messages, model=None, **kwargs):
        """Génère une réponse de chat en utilisant OpenAI."""
        model = model or config.OPENAI_MODELS["primary"]
        
        # Fusion des paramètres par défaut avec les paramètres personnalisés
        payload = {
            "model": model,
            "messages": messages,
            **{k: v for k, v in config.DEFAULT_CONFIG.items() if k != "timeout"},
            **kwargs
        }

        start_time = time.time()
        try:
            # Exécution avec logique de retry
            response_data = execute_with_retry(self.client.post, "chat/completions", payload)
            duration = time.time() - start_time
            
            # Extraction des données et logging
            usage = response_data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            content = response_data["choices"][0]["message"]["content"]
            
            log_openai_call(model, prompt_tokens, completion_tokens, duration)
            return content

        except Exception as e:
            duration = time.time() - start_time
            log_openai_call(model, 0, 0, duration, status=f"ERROR: {str(e)}")
            raise e
