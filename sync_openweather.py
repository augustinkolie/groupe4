"""
Script pour récupérer les données de pollution directement d'OpenWeather
pour toutes les stations Guinéennes
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station, Reading
from ingestion.adapters.openweather import OpenWeatherAdapter
from django.utils import timezone
from datetime import datetime

def sync_openweather_data():
    """Récupère les données OpenWeather pour toutes les stations"""
    try:
        adapter = OpenWeatherAdapter()
        
        # Récupère toutes les stations
        stations = Station.objects.all()
        
        if not stations.exists():
            print("❌ Aucune station trouvée dans la base de données")
            return
        
        print(f"\n🌍 Récupération des données pour {stations.count()} station(s)...")
        
        for station in stations:
            print(f"\n📍 Station: {station.name} ({station.latitude}, {station.longitude})")
            
            try:
                # Récupère les données pour cette station
                payloads = adapter.fetch_data_for_location(
                    lat=station.latitude,
                    lon=station.longitude,
                    name=station.name,
                    region=station.location_description
                )
                
                if not payloads:
                    print(f"   ⚠️  Aucune donnée retournée")
                    continue
                
                # Stocke les données dans la base
                for payload in payloads:
                    reading = Reading(
                        station=station,
                        timestamp=payload.captured_at,
                        pm25=payload.measurements.pm25,
                        pm10=payload.measurements.pm10,
                        co=payload.measurements.co,
                        no2=payload.measurements.no2,
                        so2=payload.measurements.so2,
                        o3=payload.measurements.o3,
                        source_type='API',
                        source_id='openweather',
                        iqa=int(payload.measurements.pm25 * 2) if payload.measurements.pm25 else 0
                    )
                    reading.save()
                    
                    # Vérifier les alertes
                    from monitoring.utils import check_alert_rules
                    check_alert_rules(reading)
                    
                    print(f"   ✅ PM2.5: {payload.measurements.pm25} µg/m³")
                
            except Exception as e:
                print(f"   ❌ Erreur: {str(e)}")
        
        print("\n✅ Synchronisation terminée!")
        
    except ValueError as e:
        print(f"❌ Erreur de configuration: {str(e)}")
        print("Assurez-vous que OPENWEATHER_API_KEY est défini dans .env")
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == '__main__':
    sync_openweather_data()
