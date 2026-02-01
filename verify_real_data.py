import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station, Reading
from django.utils import timezone

print("=" * 80)
print("VÉRIFICATION DES DONNÉES - PROVENANCE ET INTÉGRITÉ")
print("=" * 80)

# 1. Vérifier les stations
print("\n1. STATIONS EN BASE DE DONNÉES:")
print("-" * 80)
stations = Station.objects.all()
for station in stations:
    readings_count = Reading.objects.filter(station=station).count()
    latest_reading = Reading.objects.filter(station=station).order_by('-timestamp').first()
    print(f"\n📍 {station.name}")
    print(f"   Type: {station.station_type}")
    print(f"   Coordonnées: {station.latitude}, {station.longitude}")
    print(f"   Lectures total: {readings_count}")
    if latest_reading:
        print(f"   Dernière lecture: {latest_reading.timestamp}")

# 2. Vérifier l'origine des données (source_type)
print("\n\n2. PROVENANCE DES DONNÉES (source_type):")
print("-" * 80)
api_readings = Reading.objects.filter(source_type='API')
sensor_readings = Reading.objects.filter(source_type='SENSOR')
print(f"📡 Lectures de l'API OpenWeather: {api_readings.count()}")
print(f"🔌 Lectures de capteurs physiques: {sensor_readings.count()}")

# 3. Vérifier les source_id
print("\n3. DÉTAILS DE LA SOURCE:")
print("-" * 80)
latest_5_api = Reading.objects.filter(source_type='API').order_by('-timestamp')[:5]
for reading in latest_5_api:
    print(f"\n   Station: {reading.station.name}")
    print(f"   Source: {reading.source_type}")
    print(f"   Source ID: {reading.source_id}")
    print(f"   Timestamp: {reading.timestamp}")
    print(f"   PM2.5: {reading.pm25} µg/m³")
    print(f"   CO: {reading.co} mg/m³")
    print(f"   IQA: {reading.iqa}")

# 4. Vérifier la validité des données (pas de NULL abusifs)
print("\n\n4. INTÉGRITÉ DES DONNÉES:")
print("-" * 80)
latest_reading = Reading.objects.order_by('-timestamp').first()
if latest_reading:
    print(f"\nDernière lecture de la DB:")
    print(f"  Station: {latest_reading.station.name}")
    print(f"  Timestamp: {latest_reading.timestamp}")
    print(f"  PM2.5: {latest_reading.pm25}")
    print(f"  PM10: {latest_reading.pm10}")
    print(f"  CO: {latest_reading.co}")
    print(f"  NO2: {latest_reading.no2}")
    print(f"  SO2: {latest_reading.so2}")
    print(f"  O3: {latest_reading.o3}")
    print(f"  Humidity: {latest_reading.humidity}")
    print(f"  Temperature: {latest_reading.temperature}")
    print(f"  IQA: {latest_reading.iqa}")
    print(f"  Source: {latest_reading.source_type} (ID: {latest_reading.source_id})")

print("\n" + "=" * 80)
print("✅ VÉRIFICATION TERMINÉE")
print("=" * 80)
