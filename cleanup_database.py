import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station, Reading

print("=== NETTOYAGE DE LA BASE DE DONNÉES ===\n")

# 1. Supprimer tous les relevés
readings_deleted = Reading.objects.all().delete()
print(f"[OK] Releves supprimes: {readings_deleted[0]}")

# 2. Supprimer toutes les stations
stations_deleted = Station.objects.all().delete()
print(f"[OK] Stations supprimees: {stations_deleted[0]}")

# 3. Recréer uniquement les 4 stations principales de Guinée
stations_propres = [
    {
        "name": "Conakry (Centre)",
        "latitude": 9.537,
        "longitude": -13.677,
        "station_type": "VIRTUAL",
        "location_description": "Capitale de la Guinée, zone urbaine dense."
    },
    {
        "name": "Labé (Fouta)",
        "latitude": 11.318,
        "longitude": -12.283,
        "station_type": "VIRTUAL",
        "location_description": "Région de Moyenne-Guinée, climat tempéré."
    },
    {
        "name": "Kankan (Savouré)",
        "latitude": 10.385,
        "longitude": -9.305,
        "station_type": "VIRTUAL",
        "location_description": "Haute-Guinée, zone de savane."
    },
    {
        "name": "N'Zérékoré (Forêt)",
        "latitude": 7.756,
        "longitude": -8.818,
        "station_type": "VIRTUAL",
        "location_description": "Guinée Forestière, zone humide."
    }
]

for station_data in stations_propres:
    Station.objects.create(**station_data)
    print(f"[OK] Station creee: {station_data['name']}")

print(f"\n=== RÉSULTAT ===")
print(f"Total stations: {Station.objects.count()}")
print(f"Total relevés: {Reading.objects.count()}")
print("\nBase de données nettoyée avec succès!")
