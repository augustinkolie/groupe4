import os
import google.generativeai as genai
from .config import DEFAULT_CONFIG
from .safety_config import SAFETY_SETTINGS

class GeminiClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GOOGLE_GENAI_API_KEY', '').strip()
        if not self.api_key:
            raise ValueError("GOOGLE_GENAI_API_KEY non configurée.")
        
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
