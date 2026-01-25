import logging
from typing import List
from django.utils import timezone
from monitoring.models import Station, Reading
from ingestion.adapters.base import UnifiedPayload
from core.aqi import calculate_global_aqi

logger = logging.getLogger(__name__)

class IngestionService:
    """
    Orchestrates the ingestion flow: Validation -> Normalization -> Persistence.
    """
    
    def ingest_payloads(self, payloads: List[UnifiedPayload]):
        """ Processes a list of normalized payloads and saves them to DB. """
        for payload in payloads:
            try:
                # 1. Get or Create Station
                station, created = Station.objects.get_or_create(
                    latitude=payload.location.lat,
                    longitude=payload.location.lon,
                    defaults={
                        'name': payload.location.name,
                        'station_type': 'VIRTUAL' if payload.source_type == 'API' else 'PHYSICAL',
                        'metadata': {'region': payload.location.region}
                    }
                )
                
                # 2. Duplicate Detection (Simplified for SQLite)
                # Check if a reading already exists for this station at this exact timestamp
                if Reading.objects.filter(station=station, timestamp=payload.captured_at).exists():
                    continue
                
                # 3. AQI Calculation
                # Prepare measurements for AQI calculator
                measurements_dict = {
                    'pm25': payload.measurements.pm25,
                    'pm10': payload.measurements.pm10,
                    'co': payload.measurements.co
                }
                aqi_value = calculate_global_aqi(measurements_dict)
                
                # 4. Save Reading
                Reading.objects.create(
                    station=station,
                    timestamp=payload.captured_at,
                    pm25=payload.measurements.pm25,
                    pm10=payload.measurements.pm10,
                    co=payload.measurements.co,
                    no2=payload.measurements.no2,
                    so2=payload.measurements.so2,
                    o3=payload.measurements.o3,
                    humidity=payload.measurements.humidity,
                    temperature=payload.measurements.temperature,
                    iqa=aqi_value,
                    source_type=payload.source_type,
                    source_id=payload.source_id
                )
                
            except Exception as e:
                logger.error(f"Error ingesting payload for {payload.location.name}: {str(e)}")
