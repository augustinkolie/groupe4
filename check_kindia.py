import requests
import json
from django.conf import settings
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

def get_kindia_realtime():
    api_key = settings.OPENWEATHER_API_KEY
    lat, lon = 10.056, -12.865 # Kindia coordinates
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    
    print(f"Interrogation de l'API OpenWeather pour Kindia ({lat}, {lon})...")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        components = data['list'][0]['components']
        aqi_index = data['list'][0]['main']['aqi']
        
        print("\n--- DONNÉES RÉELLES KINDIA (via OpenWeather) ---")
        print(f"Indice Qualité Air (1-5): {aqi_index}")
        print(f"PM2.5: {components['pm2_5']} µg/m³")
        print(f"PM10: {components['pm10']} µg/m³")
        print(f"CO: {components['co']} µg/m³")
        print(f"NO2: {components['no2']} µg/m³")
        print(f"SO2: {components['so2']} µg/m³")
        print(f"O3: {components['o3']} µg/m³")
        print("----------------------------------------------")
    else:
        print(f"Erreur API: {response.status_code} - {response.text}")

if __name__ == "__main__":
    get_kindia_realtime()
