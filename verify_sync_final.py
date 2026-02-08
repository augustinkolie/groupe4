import os
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Reading
from django_q.models import Success
from django.utils import timezone

last_reading = Reading.objects.order_by('-timestamp').first()
success_task = Success.objects.order_by('-stopped').first()

print(f"--- Rapport de Synchronisation ---")
if success_task:
    print(f"Dernière tâche réussie : {success_task.name} à {success_task.stopped}")
else:
    print("Aucune tâche réussie trouvée dans Success.")

if last_reading:
    print(f"Dernier relevé en base : {last_reading.timestamp}")
    diff = timezone.now() - last_reading.timestamp
    if diff < timedelta(minutes=15):
        print(f"SUCCÈS : Données récentes (il y a {diff.seconds // 60} min).")
    else:
        print(f"INFO : Dernières données datent de {diff.seconds // 3600}h { (diff.seconds % 3600) // 60}min.")
else:
    print("Aucun relevé trouvé dans la base de données.")
