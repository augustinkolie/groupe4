from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="Image illustrative de la zone")
    pollution_causes = models.TextField(blank=True, null=True, help_text="Causes principales de la pollution")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Reading(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    pm25 = models.FloatField(help_text="Particulate Matter PM2.5")
    pm10 = models.FloatField(help_text="Particulate Matter PM10")
    co = models.FloatField(help_text="Carbon Monoxide (ppm)")
    humidity = models.FloatField()
    temperature = models.FloatField()
    iqa = models.IntegerField(null=True, blank=True, help_text="Air Quality Index")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Reading from {self.station.name} at {self.timestamp}"
