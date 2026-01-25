from rest_framework import viewsets, permissions, views, response, status
from django.utils import timezone
from monitoring.models import Station, Reading, Sensor
from api.serializers import StationSerializer, ReadingSerializer
from api.auth import SensorAPIKeyAuthentication
from ingestion.service import IngestionService
from ingestion.adapters.base import UnifiedPayload, UnifiedLocation, UnifiedMeasurement

class StationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows stations to be viewed.
    """
    queryset = Station.objects.all().order_by('name')
    serializer_class = StationSerializer
    permission_classes = [permissions.AllowAny]

class ReadingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows readings to be viewed.
    """
    queryset = Reading.objects.all().order_by('-timestamp')
    serializer_class = ReadingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        station_id = self.request.query_params.get('station', None)
        if station_id is not None:
            queryset = queryset.filter(station_id=station_id)
        return queryset

class SensorIngestView(views.APIView):
    """
    Endpoint for physical sensors to post data.
    Requires X-Sensor-Key header.
    """
    authentication_classes = [SensorAPIKeyAuthentication]
    permission_classes = [permissions.IsAuthenticated] # IsAuthenticated checks for (sensor, None)

    def post(self, request):
        sensor = request.user # This is the Sensor object from auth.py
        data = request.data
        
        try:
            # Reconstruct UnifiedPayload from raw data
            # Assuming sensor sends a JSON matching UnifiedMeasurement fields
            payload = UnifiedPayload(
                location=UnifiedLocation(
                    lat=sensor.station.latitude,
                    lon=sensor.station.longitude,
                    name=sensor.station.name
                ),
                measurements=UnifiedMeasurement(**data.get('measurements', {})),
                source_type="SENSOR",
                source_id=sensor.sensor_id,
                captured_at=timezone.now()
            )
            
            service = IngestionService()
            service.ingest_payloads([payload])
            
            # Update last_seen
            sensor.last_seen = timezone.now()
            sensor.save(update_fields=['last_seen'])
            
            return response.Response({"status": "success"}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return response.Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class TriggerFetchView(views.APIView):
    """
    Manually triggers the air quality data fetching from OpenWeather.
    """
    permission_classes = [permissions.AllowAny] # In production, restrict this!

    def post(self, request):
        from ingestion.management.commands.fetch_air_quality import Command
        try:
            cmd = Command()
            cmd.handle()
            return response.Response({"status": "success", "message": "Data fetch triggered"}, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
