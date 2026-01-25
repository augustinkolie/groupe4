import requests
from datetime import datetime
from typing import List, Optional
from django.conf import settings
from ingestion.adapters.base import BaseAdapter, UnifiedPayload, UnifiedLocation, UnifiedMeasurement

class OpenWeatherAdapter(BaseAdapter):
    """
    Adapter for OpenWeather Air Pollution API.
    URL: http://api.openweathermap.org/data/2.5/air_pollution
    """
    
    BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or getattr(settings, 'OPENWEATHER_API_KEY', None)
        if not self.api_key:
            raise ValueError("OpenWeather API Key is missing. Please add OPENWEATHER_API_KEY to your settings.")

    def fetch_data_for_location(self, lat: float, lon: float, name: str, region: str = None) -> List[UnifiedPayload]:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        payloads = []
        for item in data.get('list', []):
            components = item.get('components', {})
            payloads.append(UnifiedPayload(
                location=UnifiedLocation(
                    lat=lat,
                    lon=lon,
                    name=name,
                    region=region
                ),
                measurements=UnifiedMeasurement(
                    pm25=components.get('pm2_5'),
                    pm10=components.get('pm10'),
                    co=components.get('co'),
                    no2=components.get('no2'),
                    so2=components.get('so2'),
                    o3=components.get('o3')
                ),
                source_type="API",
                source_id="openweather",
                captured_at=datetime.fromtimestamp(item.get('dt'))
            ))
            
        return payloads

    def fetch_data(self) -> List[UnifiedPayload]:
        # This is a placeholder since this adapter needs specific coords.
        # In a real scenario, we would loop through all registered virtual stations.
        return []
