import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station

# Mapping des noms de stations vers leurs images locales
STATION_IMAGE_MAP = {
    'Kindia': '/static/monitoring/images/kindia.png',
    'Kindia (Cité des Agrumes)': '/static/monitoring/images/kindia.png',
    'Kankan': '/static/monitoring/images/kankan.png',
    'Kankan (Savouré)': '/static/monitoring/images/kankan.png',
    'Conakry': '/static/monitoring/images/conakry.png',
    'Conakry (Centre)': '/static/monitoring/images/conakry.png',
    'Labé': '/static/monitoring/images/labe.png',
    'Labé (Fouta)': '/static/monitoring/images/labe.png',
    'N\'Zérékoré': '/static/monitoring/images/nzerekore.png',
    'N\'Zérékoré (Forêt)': '/static/monitoring/images/nzerekore.png',
}

def update_station_images():
    """Met à jour les URLs des images pour utiliser les images locales"""
    
    print("🔄 Mise à jour des images des stations...")
    print("=" * 60)
    
    stations = Station.objects.all()
    updated_count = 0
    
    for station in stations:
        # Chercher une correspondance exacte ou partielle
        image_url = None
        
        # Correspondance exacte
        if station.name in STATION_IMAGE_MAP:
            image_url = STATION_IMAGE_MAP[station.name]
        else:
            # Correspondance partielle (ex: "Kindia" dans "Kindia (Cité des Agrumes)")
            for station_key, image_path in STATION_IMAGE_MAP.items():
                if station.name.startswith(station_key.split('(')[0].strip()):
                    image_url = image_path
                    break
        
        if image_url:
            old_url = station.image_url
            station.image_url = image_url
            station.save()
            updated_count += 1
            
            print(f"✅ {station.name}")
            print(f"   Ancien: {old_url if old_url else 'Aucune'}")
            print(f"   Nouveau: {image_url}")
            print()
        else:
            print(f"⚠️  {station.name} - Aucune image locale trouvée")
            print()
    
    print("=" * 60)
    print(f"✨ Terminé ! {updated_count} station(s) mise(s) à jour.")
    print("\nImages disponibles dans monitoring/static/monitoring/images/:")
    print("  - kindia.png")
    print("  - kankan.png") 
    print("  - conakry.png")
    print("  - labe.png")
    print("  - nzerekore.png")

if __name__ == '__main__':
    update_station_images()
