import os
from django.conf import settings
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Reading, Station, GeneratedReport

print("--- Diagnosis of Readings ---")
count = Reading.objects.count()
print(f"Total Readings: {count}")

if count > 0:
    first = Reading.objects.order_by('timestamp').first()
    last = Reading.objects.order_by('timestamp').last()
    print(f"Date Range: {first.timestamp} TO {last.timestamp}")
    
    unique_dates = Reading.objects.datetimes('timestamp', 'day')
    print(f"Unique Days with data: {[d.strftime('%Y-%m-%d') for d in unique_dates]}")

stations = Station.objects.all()
for s in stations:
    s_count = Reading.objects.filter(station=s).count()
    print(f"Station ID {s.id} - '{s.name}': {s_count} readings")

print("\n--- Last 5 Generated Reports ---")
last_reports = GeneratedReport.objects.all().order_by('-created_at')[:5]
for r in last_reports:
    print(f"Report ID {r.id}: {r.report_type} | {r.start_date} to {r.end_date}")
    print(f"  Stations included: {r.stations_included}")
    print(f"  File path: {r.file_path}")
    # Check if file exists
    full_path = os.path.join(settings.MEDIA_ROOT, r.file_path)
    exists = os.path.exists(full_path)
    size = os.path.getsize(full_path) if exists else 0
    print(f"  Exists: {exists} | Size: {size} bytes")
