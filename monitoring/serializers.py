from rest_framework import serializers
from .models import Station, Reading

class StationSerializer(serializers.ModelSerializer):
    latest_reading = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = ['id', 'name', 'latitude', 'longitude', 'station_type', 'location_description', 'latest_reading']

    def get_latest_reading(self, obj):
        recent = obj.readings.first()
        if recent:
            return ReadingSerializer(recent).data
        return None

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = [
            'id', 'timestamp', 'pm25', 'pm10', 'co', 'no2', 'so2', 'o3', 
            'humidity', 'temperature', 'iqa', 'source_type', 'source_id'
        ]

