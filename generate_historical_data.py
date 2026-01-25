import os
import django
from datetime import timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station, Reading
from django.utils import timezone

def generate_historical_data():
    """
    Génère des données historiques pour chaque station
    sur les dernières 24 heures (un point toutes les heures)
    """
    print("Génération de données historiques...")
    
    stations = Station.objects.all()
    now = timezone.now()
    
    total_created = 0
    
    for station in stations:
        print(f"\nGénération pour {station.name}...")
        
        # Générer 24 points de données (1 par heure sur 24h)
        for hours_ago in range(24, 0, -1):
            timestamp = now - timedelta(hours=hours_ago)
            
            # Vérifier si un relevé existe déjà à ce moment
            existing = Reading.objects.filter(
                station=station,
                timestamp=timestamp
            ).exists()
            
            if not existing:
                # Générer des valeurs réalistes mais variables
                base_iqa = random.randint(80, 150)
                
                reading = Reading.objects.create(
                    station=station,
                    timestamp=timestamp,
                    pm25=random.uniform(10, 50),
                    pm10=random.uniform(20, 80),
                    co=random.uniform(0.2, 2.0),
                    no2=random.uniform(10, 80),
                    so2=random.uniform(5, 40),
                    o3=random.uniform(20, 100),
                    humidity=random.uniform(50, 90),
                    temperature=random.uniform(22, 32),
                    iqa=base_iqa,
                    source_type='API',
                    source_id='test_data'
                )
                total_created += 1
                
                if hours_ago % 6 == 0:  # Afficher tous les 6 relevés
                    print(f"  ✓ {timestamp.strftime('%Y-%m-%d %H:%M')} - IQA: {base_iqa}")
    
    print(f"\n✅ {total_created} relevés historiques générés !")
    
    # Afficher les stats finales
    print("\n--- STATISTIQUES FINALES ---")
    for station in stations:
        count = station.readings.count()
        print(f"{station.name}: {count} relevés")
    
    print(f"\nTotal en base: {Reading.objects.count()} relevés")

if __name__ == "__main__":
    generate_historical_data()
