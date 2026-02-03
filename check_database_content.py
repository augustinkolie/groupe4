import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Reading, Station
from django.db.models import Avg, Count

print("=" * 80)
print("VÉRIFICATION COMPLÈTE DE LA BASE DE DONNÉES")
print("=" * 80)

# Statistiques globales
total_readings = Reading.objects.count()
print(f"\n📊 STATISTIQUES GLOBALES")
print(f"   Total de lectures: {total_readings}")
print(f"   Total de stations: {Station.objects.count()}")

# Détails par station
print(f"\n🏢 DÉTAILS PAR STATION")
print("-" * 80)

for station in Station.objects.all():
    print(f"\n📍 {station.name}")
    print(f"   Coordonnées: ({station.latitude}, {station.longitude})")
    
    readings = Reading.objects.filter(station=station).order_by('-timestamp')
    count = readings.count()
    print(f"   Nombre de lectures: {count}")
    
    if count > 0:
        # Dernière lecture
        latest = readings.first()
        print(f"\n   📅 Dernière lecture: {latest.timestamp.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"   ├─ IQA: {latest.iqa if latest.iqa else 'N/A'}")
        print(f"   ├─ PM2.5: {latest.pm25 if latest.pm25 else 'N/A'} µg/m³")
        print(f"   ├─ PM10: {latest.pm10 if latest.pm10 else 'N/A'} µg/m³")
        print(f"   ├─ CO: {latest.co if latest.co else 'N/A'} mg/m³")
        print(f"   ├─ NO2: {latest.no2 if latest.no2 else 'N/A'} µg/m³")
        print(f"   ├─ SO2: {latest.so2 if latest.so2 else 'N/A'} µg/m³")
        print(f"   ├─ O3: {latest.o3 if latest.o3 else 'N/A'} µg/m³")
        print(f"   ├─ Température: {latest.temperature if latest.temperature else 'N/A'}°C")
        print(f"   ├─ Humidité: {latest.humidity if latest.humidity else 'N/A'}%")
        print(f"   └─ Source: {latest.source_type}")
        
        # Moyennes
        stats = readings.aggregate(
            avg_iqa=Avg('iqa'),
            avg_pm25=Avg('pm25'),
            avg_pm10=Avg('pm10'),
            avg_co=Avg('co'),
            avg_temp=Avg('temperature'),
            avg_hum=Avg('humidity')
        )
        
        print(f"\n   📈 Moyennes sur toutes les lectures:")
        print(f"   ├─ IQA moyen: {stats['avg_iqa']:.2f}" if stats['avg_iqa'] else "   ├─ IQA moyen: N/A")
        print(f"   ├─ PM2.5 moyen: {stats['avg_pm25']:.2f} µg/m³" if stats['avg_pm25'] else "   ├─ PM2.5 moyen: N/A")
        print(f"   ├─ PM10 moyen: {stats['avg_pm10']:.2f} µg/m³" if stats['avg_pm10'] else "   ├─ PM10 moyen: N/A")
        print(f"   ├─ CO moyen: {stats['avg_co']:.2f} mg/m³" if stats['avg_co'] else "   ├─ CO moyen: N/A")
        print(f"   ├─ Température moyenne: {stats['avg_temp']:.1f}°C" if stats['avg_temp'] else "   ├─ Température moyenne: N/A")
        print(f"   └─ Humidité moyenne: {stats['avg_hum']:.1f}%" if stats['avg_hum'] else "   └─ Humidité moyenne: N/A")
        
        # 3 dernières lectures
        print(f"\n   🔍 3 dernières lectures:")
        for i, reading in enumerate(readings[:3], 1):
            print(f"   {i}. {reading.timestamp.strftime('%d/%m/%Y %H:%M')} - IQA: {reading.iqa if reading.iqa else 'N/A'}, PM2.5: {reading.pm25 if reading.pm25 else 'N/A'}")
    else:
        print("   ⚠️ Aucune donnée disponible")

# Vérification de la source des données
print(f"\n" + "=" * 80)
print("📡 SOURCE DES DONNÉES")
print("-" * 80)

source_counts = Reading.objects.values('source_type').annotate(count=Count('id'))
for source in source_counts:
    print(f"   {source['source_type']}: {source['count']} lectures")

# Vérification des données manquantes
print(f"\n" + "=" * 80)
print("⚠️ DONNÉES MANQUANTES")
print("-" * 80)

null_checks = {
    'iqa': Reading.objects.filter(iqa__isnull=True).count(),
    'pm25': Reading.objects.filter(pm25__isnull=True).count(),
    'pm10': Reading.objects.filter(pm10__isnull=True).count(),
    'co': Reading.objects.filter(co__isnull=True).count(),
    'temperature': Reading.objects.filter(temperature__isnull=True).count(),
    'humidity': Reading.objects.filter(humidity__isnull=True).count(),
}

for field, count in null_checks.items():
    if count > 0:
        percentage = (count / total_readings * 100) if total_readings > 0 else 0
        print(f"   {field}: {count} valeurs manquantes ({percentage:.1f}%)")

if all(count == 0 for count in null_checks.values()):
    print("   ✅ Aucune donnée manquante!")

print("\n" + "=" * 80)
