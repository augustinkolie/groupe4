import requests
import json
import time

def test_sensor_ingest():
    url = "http://127.0.0.1:8000/api/v1/ingest/sensor/"
    # Note: You need to create a Sensor in Django Admin first and get its API Key
    # Or we can create one via a shell script for testing.
    
    headers = {
        "X-Sensor-Key": "test_secret_key_123",
        "Content-Type": "application/json"
    }
    
    payload = {
        "measurements": {
            "pm25": 12.5,
            "pm10": 25.0,
            "co": 0.5,
            "humidity": 45.0,
            "temperature": 28.5
        }
    }
    
    print(f"Sending data to {url}...")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Create test data first if needed
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
    django.setup()
    
    from monitoring.models import Station, Sensor
    station, _ = Station.objects.get_or_create(name="Test Station Labé", latitude=11.318, longitude=-12.283)
    Sensor.objects.get_or_create(sensor_id="ESP32_LABE_01", station=station, api_key="test_secret_key_123")
    
    test_sensor_ingest()
