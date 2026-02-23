import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

class GeminiKeyManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiKeyManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Charge toutes les clés Gemini depuis les variables d'environnement."""
        self.keys = []
        self.current_key_index = 0
        
        # 1. Clé principale
        main_key = os.getenv('GOOGLE_GENAI_API_KEY')
        if main_key and main_key != 'votre_cle_principale_ici':
            self.keys.append(main_key)
            
        # 2. Clés secondaires (GOOGLE_GENAI_API_KEY_2, _3, etc.)
        for i in range(2, 11):
            key = os.getenv(f'GOOGLE_GENAI_API_KEY_{i}')
            if key and 'votre' not in key:
                self.keys.append(key)
                
        if not self.keys:
            logger.error("Aucune clé API Gemini valide trouvée dans l'environnement.")
            # On ne lève plus d'exception ici pour permettre au serveur de démarrer
            # mais on garde une liste vide.
            
        logger.info(f"GeminiKeyManager initialisé avec {len(self.keys)} clé(s).")

    def get_active_key(self):
        """Retourne la clé actuellement utilisée."""
        if not self.keys:
            return None
        return self.keys[self.current_key_index]

    def switch_key(self):
        """Passe à la clé suivante dans le pool et reconfigure le SDK."""
        if len(self.keys) <= 1:
            logger.warning("Demande de rotation de clé ignorée : Une seule clé disponible.")
            return False

        previous_index = self.current_key_index
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        
        new_key = self.get_active_key()
        
        # Reconfiguration globale de genai (important !)
        genai.configure(api_key=new_key)
        
        logger.warning(f"Rotation de clé effectuée : Clé #{previous_index + 1} -> Clé #{self.current_key_index + 1}")
        return True
