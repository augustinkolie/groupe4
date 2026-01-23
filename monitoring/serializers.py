from rest_framework import serializers
from .models import Station, Reading

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class ReadingSerializer(serializers.ModelSerializer):
    class NameSerializer(serializers.ModelSerializer):
        class Meta:
            model = Station
            fields = ['name']
    
    station_name = serializers.CharField(source='station.name', read_only=True)

    class Meta:
        model = Reading
        fields = '__all__'
