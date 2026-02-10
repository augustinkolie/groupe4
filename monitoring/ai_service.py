import requests
import json
import os
from django.conf import settings

class AIService:
    def __init__(self):
        # Récupération de la clé API et nettoyage des espaces
        self.api_key = os.getenv('GOOGLE_GENAI_API_KEY', '').strip()
        # Note: gemini-1.5-flash renvoie 404 sur ce compte, utilisation de 2.0-flash (stable)
        self.model_name = "gemini-2.0-flash"

    def _get_api_url(self):
        # Endpoint officiel tel que demandé : v1 avec le modèle spécifié
        return f"https://generativelanguage.googleapis.com/v1/models/{self.model_name}:generateContent?key={self.api_key}"

    def _get_headers(self):
        return {
            "Content-Type": "application/json"
        }

    def _handle_api_error(self, response):
        """Gère les erreurs HTTP courantes avec des messages explicites."""
        if response.status_code == 429:
            return "Erreur 429 : Trop de requêtes. La limite gratuite de l'API Gemini est atteinte. Veuillez patienter une minute avant de réessayer."
        elif response.status_code == 404:
            return "Erreur 404 : L'endpoint de l'API Gemini ou le modèle est introuvable. Vérifiez l'URL."
        elif response.status_code == 401:
            return "Erreur 401 : Clé API non valide. Vérifiez votre clé GOOGLE_GENAI_API_KEY dans le fichier .env."
        elif response.status_code == 403:
            return "Erreur 403 : Accès refusé. Assurez-vous que l'API est activée pour ce projet dans la console Google Cloud."
        else:
            return f"Erreur {response.status_code} : Une erreur inattendue est survenue (Client Error: {response.reason})"

    def get_chat_response(self, user_message, context=""):
        if not self.api_key:
            return "Configuration requise : La clé API Google Gemini n'est pas configurée. Veuillez l'ajouter à votre fichier .env."
        
        system_prompt = f"""
        Tu es l'assistant intelligent d'EcoWatch, une plateforme de surveillance de la qualité de l'air en Guinée.
        Ton but est d'aider les visiteurs à comprendre les données environnementales et à adopter des comportements sains.
        
        Contexte :
        {context}
        
        Réponds de manière concise, professionnelle et amicale en français.
        """
        
        payload = {
            "contents": [
                {
                    "parts": [
                        { "text": f"{system_prompt}\n\nUtilisateur: {user_message}" }
                    ]
                }
            ]
        }
        
        try:
            url = self._get_api_url()
            headers = self._get_headers()
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            
            if response.status_code != 200:
                return self._handle_api_error(response)
                
            data = response.json()
            if 'candidates' in data and data['candidates']:
                return data['candidates'][0]['content']['parts'][0]['text']
            return "L'IA n'a pas renvoyé de contenu valide. Veuillez réessayer."
            
        except requests.exceptions.RequestException as e:
            return f"Erreur de connexion : Impossible de joindre l'API Google ({str(e)})"
        except Exception as e:
            return f"Une erreur technique est survenue : {str(e)}"

    def analyze_readings(self, readings_data):
        if not self.api_key:
            return "Service d'analyse indisponible : Clé API manquante."
            
        payload = {
            "contents": [
                {
                    "parts": [
                        { "text": f"Analyse les mesures de qualité de l'air suivantes et donne un résumé rapide ainsi que 3 conseils de santé :\n{readings_data}" }
                    ]
                }
            ]
        }
        
        try:
            url = self._get_api_url()
            headers = self._get_headers()
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            
            if response.status_code != 200:
                return self._handle_api_error(response)
                
            data = response.json()
            if 'candidates' in data and data['candidates']:
                return data['candidates'][0]['content']['parts'][0]['text']
            return "Analyse impossible pour le moment."
            
        except Exception as e:
            return f"Erreur lors de l'analyse IA : {str(e)}"
