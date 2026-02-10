import requests
import json
import os
from django.conf import settings

class AIService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_GENAI_API_KEY')
        # Gemini 1.5 Flash API endpoint
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"

    def get_chat_response(self, user_message, context=""):
        if not self.api_key:
            return "Désolé, la clé API Gemini n'est pas configurée dans le fichier .env (GOOGLE_GENAI_API_KEY)."
        
        system_prompt = f"""
        Tu es l'assistant intelligent d'EcoWatch, une plateforme de surveillance de la qualité de l'air en Guinée.
        Ton but est d'aider les visiteurs à comprendre les données environnementales et à adopter des comportements sains.
        
        Données actuelles ou contexte du projet :
        {context}
        
        Réponds de manière concise, professionnelle et amicale en français. 
        Si on te pose des questions hors du sujet de l'environnement ou du projet EcoWatch, redirige gentiment la conversation vers la qualité de l'air.
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": f"{system_prompt}\n\nUtilisateur: {user_message}"}]
            }]
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Extract text from Gemini response structure
            if 'candidates' in data and len(data['candidates']) > 0:
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Je n'ai pas pu générer de réponse. Veuillez réessayer."
        except Exception as e:
            return f"Une erreur est survenue lors de la communication avec l'IA : {str(e)}"

    def analyze_readings(self, readings_data):
        if not self.api_key:
            return "Service IA non disponible (Clé API manquante)."
            
        prompt = f"""
        Analyse les mesures de qualité de l'air suivantes et donne un résumé rapide ainsi que 3 conseils de santé :
        {readings_data}
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if 'candidates' in data and len(data['candidates']) > 0:
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Analyse impossible pour le moment."
        except Exception as e:
            return f"Erreur d'analyse : {str(e)}"
