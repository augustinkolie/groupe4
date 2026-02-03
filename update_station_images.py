import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station

# URLs d'images Unsplash pour chaque ville
images = {
    "Conakry (Centre)": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?auto=format&fit=crop&w=800&q=80",  # City traffic
    "Labé (Fouta)": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=800&q=80",  # Mountain landscape
    "Kankan (Savouré)": "https://images.unsplash.com/photo-1469022563149-aa64dbd37dae?auto=format&fit=crop&w=800&q=80",  # Savanna
    "N'Zérékoré (Forêt)": "https://images.unsplash.com/photo-1511497584788-876760111969?auto=format&fit=crop&w=800&q=80",  # Forest
}

print("Mise à jour des images des stations...\n")
for station_name, image_url in images.items():
    try:
        station = Station.objects.get(name=station_name)
        station.image_url = image_url
        station.save()
        print(f"✅ {station_name}")
        print(f"   Image: {image_url}\n")
    except Station.DoesNotExist:
        print(f"❌ {station_name} - Station introuvable\n")

print("✅ Mise à jour terminée !")
