import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Reading, Station
from django.db.models import Min, Max
from datetime import datetime

print("=" * 60)
print("DIAGNOSTIC DES LECTURES")
print("=" * 60)

total_readings = Reading.objects.count()
print(f"\n📊 Total de lectures: {total_readings}")

if total_readings > 0:
    # Plage de dates
    date_range = Reading.objects.aggregate(
        min_date=Min('timestamp'),
        max_date=Max('timestamp')
    )
    print(f"\n📅 Plage de dates:")
    print(f"   Plus ancienne: {date_range['min_date']}")
    print(f"   Plus récente: {date_range['max_date']}")
    
    # Par station
    print(f"\n🏢 Répartition par station:")
    for station in Station.objects.all():
        count = Reading.objects.filter(station=station).count()
        if count > 0:
            latest = Reading.objects.filter(station=station).order_by('-timestamp').first()
            print(f"   {station.name}: {count} lectures")
            print(f"      Dernière: {latest.timestamp.strftime('%Y-%m-%d %H:%M')}")
            print(f"      Date uniquement: {latest.timestamp.date()}")
    
    # Test de filtre par date
    print(f"\n🔍 Test de filtres:")
    test_date = datetime(2026, 2, 1).date()
    print(f"   Date de test: {test_date}")
    
    for station in Station.objects.all():
        readings_today = Reading.objects.filter(
            station=station,
            timestamp__date=test_date
        ).count()
        
        readings_gte = Reading.objects.filter(
            station=station,
            timestamp__date__gte=test_date
        ).count()
        
        if readings_today > 0 or readings_gte > 0:
            print(f"   {station.name}:")
            print(f"      Exact {test_date}: {readings_today}")
            print(f"      >= {test_date}: {readings_gte}")

else:
    print("\n⚠️ Aucune lecture dans la base de données!")

print("\n" + "=" * 60)
