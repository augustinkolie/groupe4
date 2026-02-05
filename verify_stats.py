import os
import sys
import django
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg

# Setup
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station, Reading

def check_stats():
    time_threshold = timezone.now() - timedelta(hours=24)
    total_stations = Station.objects.count()
    readings_24h = Reading.objects.filter(timestamp__gte=time_threshold).count()
    avg_iqa = Reading.objects.filter(timestamp__gte=time_threshold).aggregate(Avg('iqa'))['iqa__avg'] or 0
    
    print(f"Stations: {total_stations}")
    print(f"Readings 24h: {readings_24h}")
    print(f"Avg IQA: {avg_iqa}")

    if total_stations > 0 and readings_24h > 0:
        print("✅ Stats are functional.")
    else:
        print("❌ Stats might be empty.")

if __name__ == "__main__":
    check_stats()
