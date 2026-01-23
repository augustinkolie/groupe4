import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station, Reading
import random
from django.utils import timezone

def seed_data():
    # Stations
    stations = [
        {
            "name": "Conakry - Kaloum", 
            "lat": 9.5092, "lon": -13.7122, 
            "desc": "Centre-ville, zone administrative fortement urbanisée.",
            "img": "/brain/61fa76ee-0668-474a-afa2-9c490f0dadb7/pollution_conakry_kaloum_1769074460145.png",
            "causes": "Trafic intense, émissions de véhicules anciens, et proximité du port autonome."
        },
        {
            "name": "Conakry - Ratoma", 
            "lat": 9.5847, "lon": -13.6234, 
            "desc": "Zone résidentielle et commerciale en pleine expansion.",
            "img": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=800&q=80",
            "causes": "Déchets ménagers incinérés et forte densité de population."
        },
        {
            "name": "Kindia - Centre", 
            "lat": 10.05, "lon": -12.86, 
            "desc": "Ville carrefour majeure entre la côte et l'intérieur du pays.",
            "img": "https://images.unsplash.com/photo-1506466010722-395ee2be5c17?auto=format&fit=crop&w=800&q=80",
            "causes": "Poussière des routes non bitumées et fumées de camions de transport."
        },
        {
            "name": "Boké - Zone Industrielle", 
            "lat": 10.93, "lon": -14.29, 
            "desc": "Zone minière stratégique avec des activités d'extraction bauxite.",
            "img": "https://images.unsplash.com/photo-1581094288338-2314dddb7bc3?auto=format&fit=crop&w=800&q=80",
            "causes": "Activités minières, poussière de bauxite et camions de transport minier."
        },
        {
            "name": "Labé - Centre", 
            "lat": 11.31, "lon": -12.28, 
            "desc": "Capitale du Fouta Djallon avec un climat plus tempéré.",
            "img": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=800&q=80",
            "causes": "Feux de brousse saisonniers et fumée de charbon de bois domestique."
        },
    ]

    for s_data in stations:
        station, created = Station.objects.get_or_create(
            name=s_data["name"],
            latitude=s_data["lat"],
            longitude=s_data["lon"],
            defaults={
                "location_description": s_data["desc"],
                "image_url": s_data.get("img"),
                "pollution_causes": s_data.get("causes")
            }
        )
        if not created:
            station.image_url = s_data.get("img")
            station.pollution_causes = s_data.get("causes")
            station.location_description = s_data["desc"]
            station.save()
        
        if created:
            print(f"Created station: {station.name}")
            # Generate dummy readings
            for i in range(20):
                Reading.objects.create(
                    station=station,
                    pm25=random.uniform(10, 150),
                    pm10=random.uniform(20, 200),
                    co=random.uniform(0.5, 10),
                    humidity=random.uniform(60, 95),
                    temperature=random.uniform(25, 35),
                    iqa=random.randint(20, 180)
                )
            print(f"Added 20 readings for {station.name}")

if __name__ == "__main__":
    seed_data()
