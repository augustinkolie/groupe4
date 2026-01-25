import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from ingestion.adapters.mock_sensor import MockSensorAdapter
from ingestion.service import IngestionService

def run_test_ingestion():
    print("Starting test ingestion...")
    
    # 1. Initialize Adapter and Service
    adapter = MockSensorAdapter()
    service = IngestionService()
    
    # 2. Fetch Mock Data
    payloads = adapter.fetch_data()
    print(f"Fetched {len(payloads)} payload(s) from MockSensorAdapter.")
    
    # 3. Process Ingestion
    service.ingest_payloads(payloads)
    print("Ingestion complete.")
    
    # 4. Verify in DB
    from monitoring.models import Station, Reading
    stations_count = Station.objects.count()
    readings_count = Reading.objects.count()
    
    print(f"Stats - Stations: {stations_count}, Readings: {readings_count}")
    
    if readings_count > 0:
        latest = Reading.objects.latest('timestamp')
        print(f"Latest reading: Station={latest.station.name}, PM2.5={latest.pm25}, AQI={latest.iqa}")
    else:
        print("Error: No readings found in DB.")

if __name__ == "__main__":
    run_test_ingestion()
