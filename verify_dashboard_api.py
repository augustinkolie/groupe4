import os
import sys
import django
import json

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station
from monitoring.serializers import StationSerializer

def check_serializer():
    station = Station.objects.first()
    if not station:
        print("❌ Aucune station trouvée.")
        return

    serializer = StationSerializer(station)
    data = serializer.data
    
    print(f"Station: {data['name']}")
    if 'latest_reading' in data:
        print("✅ Champ 'latest_reading' présent.")
        if data['latest_reading']:
            print(f"   Données: PM2.5={data['latest_reading'].get('pm25')}")
        else:
             print("   ⚠️ Champ présent mais vide (pas de lectures ?)")
    else:
        print("❌ Champ 'latest_reading' MANQUANT.")

if __name__ == "__main__":
    check_serializer()
