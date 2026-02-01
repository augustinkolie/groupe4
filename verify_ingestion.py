import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from ingestion.adapters.openweather import OpenWeatherAdapter
from ingestion.service import IngestionService
from monitoring.models import Station

def run_test_ingestion():
    print("Starting test ingestion...")
    
    # 1. Initialize Adapter and Service
    adapter = OpenWeatherAdapter()
    service = IngestionService()
    
    # 2. Fetch Real Data from OpenWeather for virtual stations
    # Get all virtual stations
    virtual_stations = Station.objects.filter(station_type='VIRTUAL')
    if not virtual_stations.exists():
        print("No virtual stations found. Creating one for testing...")
        station = Station.objects.create(
            name="Conakry - Test Station",
            latitude=9.6412,
            longitude=-13.2317,
            station_type='VIRTUAL',
            location_description="Conakry, Guinea"
        )
        virtual_stations = [station]
    
    all_payloads = []
    for station in virtual_stations:
        print(f"Fetching real data for {station.name}...")
        payloads = adapter.fetch_data_for_location(
            lat=station.latitude,
            lon=station.longitude,
            name=station.name
        )
        all_payloads.extend(payloads)
    
    print(f"Fetched {len(all_payloads)} payload(s) from OpenWeatherAdapter.")
    
    # 3. Process Ingestion
    service.ingest_payloads(all_payloads)
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
