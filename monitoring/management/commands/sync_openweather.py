"""
Django management command to sync OpenWeather data for all stations
"""
from django.core.management.base import BaseCommand
from monitoring.models import Station, Reading
from ingestion.adapters.openweather import OpenWeatherAdapter
from django.utils import timezone

class Command(BaseCommand):
    help = 'Récupère les données de pollution de toutes les stations via OpenWeather API'

    def handle(self, *args, **options):
        try:
            adapter = OpenWeatherAdapter()
            
            # Récupère toutes les stations
            stations = Station.objects.all()
            
            if not stations.exists():
                self.stdout.write(self.style.ERROR('❌ Aucune station trouvée'))
                return
            
            self.stdout.write(self.style.SUCCESS(f'\n🌍 Récupération pour {stations.count()} station(s)...'))
            
            total_readings = 0
            
            for station in stations:
                self.stdout.write(f'\n📍 {station.name} ({station.latitude}, {station.longitude})')
                
                try:
                    payloads = adapter.fetch_data_for_location(
                        lat=station.latitude,
                        lon=station.longitude,
                        name=station.name,
                        region=station.location_description
                    )
                    
                    if not payloads:
                        self.stdout.write('   ⚠️  Aucune donnée')
                        continue
                    
                    for payload in payloads:
                        reading = Reading(
                            station=station,
                            timestamp=payload.captured_at,
                            pm25=payload.measurements.pm25,
                            pm10=payload.measurements.pm10,
                            co=payload.measurements.co,
                            no2=payload.measurements.no2,
                            so2=payload.measurements.so2,
                            o3=payload.measurements.o3,
                            source_type='API',
                            source_id='openweather'
                        )
                        reading.save()
                        total_readings += 1
                        
                        pm25_status = self.style.SUCCESS(f'✅')
                        self.stdout.write(f'   {pm25_status} PM2.5: {payload.measurements.pm25} µg/m³')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'   ❌ Erreur: {str(e)}'))
            
            self.stdout.write(self.style.SUCCESS(f'\n✅ {total_readings} mesures importées!'))
            
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'❌ {str(e)}'))
