import os
import django
from django.utils import timezone

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from django_q.tasks import schedule
from django_q.models import Schedule

def schedule_ingestion():
    # Nom de la fonction à exécuter
    task_func = 'monitoring.tasks.fetch_air_quality_task'

    # Vérifier si elle existe déjà pour ne pas la dupliquer
    if Schedule.objects.filter(func=task_func).exists():
        print("Une tâche d'ingestion est déjà planifiée.")
        # Optionnel : La mettre à jour si besoin
        # existing_task = Schedule.objects.get(func=task_func)
        # existing_task.minutes = 10
        # existing_task.save()
        return

    # Création de la planification (Toutes les 10 minutes)
    schedule(
        func=task_func,
        schedule_type=Schedule.MINUTES,
        minutes=10,
        repeats=-1, # Infini
        next_run=timezone.now()
    )
    print("Succès ! La tâche 'fetch_air_quality_task' a été programmée pour tourner toutes les 10 minutes.")

if __name__ == "__main__":
    schedule_ingestion()
