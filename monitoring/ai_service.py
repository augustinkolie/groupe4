import logging
import os
from .services.openai import OpenAIService
from .services.gemini import GeminiService

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Initialisation des services professionnels
        self.openai_service = OpenAIService()
        self.gemini_service = GeminiService()
        
        # Flag pour tests (Si True, force l'utilisation d'OpenAI uniquement)
        # On le remet à False pour activer la rotation automatique Pro
        self.force_openai = False 

    def get_chat_response(self, user_message, context="", history=None):
        """Gère la réponse exclusivement via Gemini (OpenAI ignoré pour le moment)."""
        logger.info("Appel du service Gemini Pro Service...")
        try:
            return self.gemini_service.get_chat_response(user_message, context, history)
        except Exception as e:
            logger.error(f"Échec Gemini : {str(e)}")
            return f"Désolé, le service Gemini est temporairement indisponible. (Détails: {str(e)})"

    def analyze_readings(self, readings_data):
        """Délègue l'analyse des relevés exclusivement à Gemini."""
        try:
            prompt = f"Analyse ces relevés de qualité de l'air et donne 3 conseils de santé courts : {readings_data}"
            return self.gemini_service.generate_content(prompt)
        except Exception as e:
            logger.error(f"Échec analyse Gemini : {str(e)}")
            return "Analyse IA (Gemini) indisponible pour le moment."
