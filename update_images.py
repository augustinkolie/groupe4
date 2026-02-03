import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station

# Mapping of station names (or partial names) to new image paths
image_updates = {
    "Conakry": "/static/monitoring/images/conakry.png",
    "Labé": "/static/monitoring/images/labe.png",
    "Kankan": "/static/monitoring/images/kankan.png",
    "N'Zérékoré": "/static/monitoring/images/nzerekore.png",
    "Kindia": "/static/monitoring/images/kindia.png"
}

print("Updating station images...")

for station in Station.objects.all():
    updated = False
    for key, path in image_updates.items():
        if key.lower() in station.name.lower():
            station.image_url = path
            station.save()
            print(f"Updated image for {station.name} to {path}")
            updated = True
            break
    
    if not updated:
        print(f"No specific image found for {station.name}, skipping.")

print("Done.")
