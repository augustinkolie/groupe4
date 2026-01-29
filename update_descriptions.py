import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station

# New descriptions
descriptions = {
    "Conakry": "Capitale animée, trafic dense et activité industrielle intense.",
    "Labé": "Zone montagneuse du Fouta, risques liés aux feux de brousse.",
    "Kankan": "Savane sèche, poussière harmattan et pollution domestique.",
    "N'Zérékoré": "Forêt dense humide, enjeux de déforestation locale.",
    "Kindia": "Cité des agrumes, carrefour commercial et agricole."
}

print("Updating station descriptions...")

for station in Station.objects.all():
    updated = False
    for key, desc in descriptions.items():
        if key.lower() in station.name.lower():
            station.location_description = desc
            station.save()
            print(f"Updated description for {station.name}")
            updated = True
            break
    
    if not updated:
        print(f"No specific description found for {station.name}")

print("Done.")
