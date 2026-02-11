from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def fetch_air_quality_task():
    """
    Tâche Django Q pour lancer la commande d'ingestion des données.
    """
    logger.info("Début de la tâche planifiée : fetch_air_quality")
    try:
        call_command('fetch_air_quality')
        logger.info("Fin de la tâche planifiée : succès")
    except Exception as e:
        logger.error(f"Erreur lors de la tâche planifiée fetch_air_quality : {str(e)}")
