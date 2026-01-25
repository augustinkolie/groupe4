from django.db import models

class Station(models.Model):
    STATION_TYPES = [
        ('PHYSICAL', 'Capteur Physique'),
        ('VIRTUAL', 'Station Virtuelle (API)'),
    ]
    name = models.CharField(max_length=100)
    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)
    station_type = models.CharField(max_length=10, choices=STATION_TYPES, default='PHYSICAL')
    location_description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="Image illustrative de la zone")
    pollution_causes = models.TextField(blank=True, null=True, help_text="Causes principales de la pollution")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Reading(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField(db_index=True)
    pm25 = models.FloatField(help_text="Particulate Matter PM2.5", null=True, blank=True)
    pm10 = models.FloatField(help_text="Particulate Matter PM10", null=True, blank=True)
    co = models.FloatField(help_text="Carbon Monoxide (ppm)", null=True, blank=True)
    no2 = models.FloatField(null=True, blank=True)
    so2 = models.FloatField(null=True, blank=True)
    o3 = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    iqa = models.IntegerField(null=True, blank=True, help_text="Air Quality Index")
    
    # Métadonnées de traçabilité
    source_type = models.CharField(max_length=10, choices=[('API', 'API'), ('SENSOR', 'Capteur')], default='API')
    source_id = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['station', '-timestamp']),
        ]

    def __str__(self):
        return f"Reading from {self.station.name} at {self.timestamp}"

class Sensor(models.Model):
    sensor_id = models.CharField(max_length=50, unique=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='sensors')
    api_key = models.CharField(max_length=100, unique=True)
    hardware_type = models.CharField(max_length=50, blank=True) # e.g. "ESP32"
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Sensor {self.sensor_id} ({self.station.name})"
