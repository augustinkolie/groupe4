from django.core.management.base import BaseCommand
from monitoring.models import Station
from ingestion.adapters.openweather import OpenWeatherAdapter
from ingestion.service import IngestionService
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetches latest air quality data for all virtual stations from OpenWeather API'

    def handle(self, *args, **options):
        # 1. Get all virtual stations (or those with specific metadata)
        stations = Station.objects.filter(station_type='VIRTUAL')
        
        if not stations.exists():
            self.stdout.write(self.style.WARNING("No virtual stations found. Please create one with coordinates first."))
            return

        try:
            adapter = OpenWeatherAdapter()
            service = IngestionService()
            
            total_ingested = 0
            for station in stations:
                self.stdout.write(f"Fetching data for {station.name}...")
                payloads = adapter.fetch_data_for_location(
                    lat=station.latitude,
                    lon=station.longitude,
                    name=station.name
                )
                service.ingest_payloads(payloads)
                total_ingested += len(payloads)
                
            self.stdout.write(self.style.SUCCESS(f"Successfully ingested {total_ingested} measurements."))
            
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
