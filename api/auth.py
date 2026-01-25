from rest_framework import authentication, exceptions
from monitoring.models import Sensor

class SensorAPIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_SENSOR_KEY')
        if not api_key:
            return None

        try:
            sensor = Sensor.objects.get(api_key=api_key, is_active=True)
        except Sensor.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid or inactive sensor key.')

        return (sensor, None)
