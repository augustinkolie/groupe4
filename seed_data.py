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
            "desc": "Centre-ville, zone administrative et portuaire.",
            "img": "https://images.unsplash.com/photo-1596416608554-73479cecc40d?auto=format&fit=crop&w=800&q=80",
            "causes": "Trafic intense, émissions de véhicules anciens, et poussière portuaire."
        },
        {
            "name": "Conakry - Ratoma", 
            "lat": 9.5847, "lon": -13.6234, 
            "desc": "Zone résidentielle et commerciale dense.",
            "img": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=800&q=80",
            "causes": "Gestion des déchets, feux domestiques et forte densité de population."
        },
        {
            "name": "Kankan - Centre", 
            "lat": 10.3854, "lon": -9.3057, 
            "desc": "Deuxième plus grande ville, climat soudano-sahélien.",
            "img": "https://images.unsplash.com/photo-1516733962228-fabda232ec5b?auto=format&fit=crop&w=800&q=80",
            "causes": "Harmattan (vent de sable), poussière des routes et pollution urbaine."
        },
        {
            "name": "Nzérékoré - Centre", 
            "lat": 7.7562, "lon": -8.8179, 
            "desc": "Capitale de la Guinée forestière.",
            "img": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=800&q=80",
            "causes": "Déforestation, feux de brousse et activités agricoles intenses."
        },
        {
            "name": "Labé - Centre", 
            "lat": 11.31, "lon": -12.28, 
            "desc": "Ville d'altitude du Fouta Djallon.",
            "img": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=800&q=80",
            "causes": "Charbon de bois, relief montagneux piégeant les fumées matinales."
        },
        {
            "name": "Kindia - Centre", 
            "lat": 10.05, "lon": -12.86, 
            "desc": "Zone de transit majeure et cité des agrumes.",
            "img": "https://images.unsplash.com/photo-1506466010722-395ee2be5c17?auto=format&fit=crop&w=800&q=80",
            "causes": "Trafic de poids lourds et poussière routière."
        },
        {
            "name": "Boké - Zone Minière", 
            "lat": 10.93, "lon": -14.29, 
            "desc": "Zone d'extraction intensive de bauxite.",
            "img": "https://images.unsplash.com/photo-1581094288338-2314dddb7bc3?auto=format&fit=crop&w=800&q=80",
            "causes": "Poussière rouge de bauxite, engins lourds et impacts industriels."
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
