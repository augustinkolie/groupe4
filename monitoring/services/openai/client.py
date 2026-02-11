import os
import requests
from .config import DEFAULT_CONFIG
from .error_handler import handle_api_error

class OpenAIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY', '').strip()
        self.base_url = "https://api.openai.com/v1"

    def post(self, endpoint, payload):
        """Méthode de base pour envoyer une requête POST à l'API OpenAI."""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post(
            url, 
            headers=headers, 
            json=payload, 
            timeout=DEFAULT_CONFIG["timeout"]
        )
        
        if response.status_code != 200:
            raise handle_api_error(response)
            
        return response.json()
