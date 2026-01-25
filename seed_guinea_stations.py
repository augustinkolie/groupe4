import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station

def seed_stations():
    stations = [
        {
            "name": "Conakry (Centre)",
            "latitude": 9.537,
            "longitude": -13.677,
            "station_type": "VIRTUAL",
            "location_description": "Capitale de la Guinée, zone côtière."
        },
        {
            "name": "Labé (Fouta)",
            "latitude": 11.318,
            "longitude": -12.283,
            "station_type": "VIRTUAL",
            "location_description": "Moyenne Guinée, climat d'altitude."
        },
        {
            "name": "Kankan (Savouré)",
            "latitude": 10.385,
            "longitude": -9.305,
            "station_type": "VIRTUAL",
            "location_description": "Haute Guinée, zone de savane."
        },
        {
            "name": "N'Zérékoré (Forêt)",
            "latitude": 7.756,
            "longitude": -8.818,
            "station_type": "VIRTUAL",
            "location_description": "Guinée Forestière, zone humide."
        },
        {
            "name": "Kindia (Cité des Agrumes)",
            "latitude": 10.056,
            "longitude": -12.865,
            "station_type": "VIRTUAL",
            "location_description": "Zone de production agrumicole, climat doux."
        }
    ]

    print("Création des stations virtuelles en Guinée...")
    for s_data in stations:
        station, created = Station.objects.get_or_create(
            name=s_data["name"],
            defaults={
                "latitude": s_data["latitude"],
                "longitude": s_data["longitude"],
                "station_type": s_data["station_type"],
                "location_description": s_data["location_description"]
            }
        )
        if created:
            print(f" - Station '{station.name}' créée avec succès.")
        else:
            print(f" - Station '{station.name}' existe déjà.")

if __name__ == "__main__":
    seed_stations()
