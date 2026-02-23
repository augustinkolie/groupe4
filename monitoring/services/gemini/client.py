import os
import google.generativeai as genai
from .config import DEFAULT_CONFIG
from .safety_config import SAFETY_SETTINGS

from .key_manager import GeminiKeyManager

class GeminiClient:
    def __init__(self, api_key=None):
        self.key_manager = GeminiKeyManager()
        
        # Si une clé spécifique est passée, on l'utilise (rare), sinon on prend celle du manager
        self.api_key = api_key or self.key_manager.get_active_key()
        
        if not self.api_key:
            import logging
            logging.getLogger(__name__).warning("GOOGLE_GENAI_API_KEY non configurée. Les fonctionnalités IA seront désactivées.")
        else:
            # Configuration globale du SDK
            genai.configure(api_key=self.api_key)

    def get_model(self, model_name):
        """Initialise et configure le modèle génératif."""
        generation_config = {
            "temperature": DEFAULT_CONFIG["temperature"],
            "top_p": DEFAULT_CONFIG["top_p"],
            "top_k": DEFAULT_CONFIG["top_k"],
            "max_output_tokens": DEFAULT_CONFIG["max_output_tokens"],
        }
        
        return genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings=SAFETY_SETTINGS
        )
