import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station, Reading

print("=== DIAGNOSTIC COMPLET ===\n")

# 1. Stations
stations = Station.objects.all()
print(f"[1] Stations en base: {stations.count()}")
for s in stations:
    readings_count = s.readings.count()
    print(f"    - {s.name}: {readings_count} releves")

# 2. Relevés
readings = Reading.objects.all()
print(f"\n[2] Total releves: {readings.count()}")

if readings.exists():
    r = readings.order_by('-timestamp').first()
    print(f"\n[3] Dernier releve ingere:")
    print(f"    Station: {r.station.name}")
    print(f"    Timestamp: {r.timestamp}")
    print(f"    PM2.5: {r.pm25}")
    print(f"    NO2: {r.no2}")
    print(f"    SO2: {r.so2}")
    print(f"    O3: {r.o3}")
    print(f"    IQA: {r.iqa}")
    print(f"    Temperature: {r.temperature}")
    print(f"    Humidite: {r.humidity}")
else:
    print("\n[3] AUCUN RELEVE TROUVE!")
    print("    >> Vous devez lancer: python manage.py fetch_air_quality")
