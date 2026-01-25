from rest_framework import serializers
from monitoring.models import Station, Reading

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = [
            'id', 'timestamp', 'pm25', 'pm10', 'co', 'no2', 'so2', 'o3', 
            'humidity', 'temperature', 'iqa', 'source_type', 'source_id'
        ]

class StationSerializer(serializers.ModelSerializer):
    latest_reading = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = [
            'id', 'name', 'latitude', 'longitude', 'station_type', 
            'location_description', 'image_url', 'pollution_causes', 
            'metadata', 'created_at', 'latest_reading'
        ]

    def get_latest_reading(self, obj):
        reading = obj.readings.order_by('-timestamp').first()
        if reading:
            return ReadingSerializer(reading).data
        return None
