import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station

# Nouvelle image pour Kankan (savane africaine)
station = Station.objects.get(name__contains="Kankan")
station.image_url = "https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=800&q=80"
station.save()

print("Image de Kankan mise a jour")
print(f"Nouvelle URL: {station.image_url}")
