import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station, Reading

def diagnostic():
    print("--- DIAGNOSTIC DATA ---")
    stations = Station.objects.all()
    print(f"Nombre de Stations: {stations.count()}")
    
    for s in stations:
        latest = s.readings.order_by('-timestamp').first()
        if latest:
            print(f"Station: {s.name}")
            print(f"  - Dernier relevé: {latest.timestamp}")
            print(f"  - IQA: {latest.iqa}")
            print(f"  - Source: {latest.source_type} ({latest.source_id})")
        else:
            print(f"Station: {s.name} - Aucun relevé")

    total_readings = Reading.objects.count()
    print(f"\nTotal des relevés en base: {total_readings}")
    
    # Check today's readings (ignoring timezone for a moment to be sure)
    readings_today = Reading.objects.filter(timestamp__gte=timezone.now() - timezone.timedelta(days=1)).count()
    print(f"Relevés des dernières 24h: {readings_today}")

if __name__ == "__main__":
    diagnostic()
