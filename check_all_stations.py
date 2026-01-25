import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station, Reading

print("=== DÉTAILS DE CHAQUE STATION ===\n")

stations = Station.objects.all().order_by('id')

for station in stations:
    readings = station.readings.all().order_by('-timestamp')[:5]
    print(f"📍 Station ID: {station.id} - {station.name}")
    print(f"   Total relevés: {station.readings.count()}")
    
    if readings:
        print(f"   Derniers relevés:")
        for reading in readings:
            print(f"      - {reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | IQA: {reading.iqa}")
    else:
        print(f"   ⚠️  Aucun relevé")
    print()
