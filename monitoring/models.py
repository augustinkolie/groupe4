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
    image = models.ImageField(upload_to='stations/', blank=True, null=True, help_text="Image illustrative de la zone")
    image_url = models.URLField(blank=True, null=True, help_text="URL de l'image (obsolète)")
    pollution_causes = models.TextField(blank=True, null=True, help_text="Causes principales de la pollution")
    sensors_count = models.IntegerField(default=0, null=True, blank=True, help_text="Nombre de capteurs installés sur cette station")
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

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class AlertRule(models.Model):
    # Seuils (None = pas de seuil)
    iqa_threshold = models.IntegerField(null=True, blank=True, help_text="Seuil IQA (ex: 100)")
    pm25_threshold = models.FloatField(null=True, blank=True, help_text="Seuil PM2.5 en µg/m³")
    co_threshold = models.FloatField(null=True, blank=True, help_text="Seuil CO en µg/m³")
    temperature_threshold = models.FloatField(null=True, blank=True, help_text="Seuil Température en °C")
    
    # Notifications
    email_notification = models.BooleanField(default=True)
    email_address = models.EmailField(blank=True, null=True)
    sms_notification = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Métadonnées
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Règle d'alerte ({'Active' if self.is_active else 'Inactive'})"

class AlertLog(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='alerts')
    rule = models.ForeignKey(AlertRule, on_delete=models.SET_NULL, null=True)
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE, related_name='triggered_alerts')
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerte {self.station.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
class GeneratedReport(models.Model):
    REPORT_TYPES = [
        ('DAILY', 'Quotidien'),
        ('WEEKLY', 'Hebdomadaire'),
        ('MONTHLY', 'Mensuel'),
        ('ANNUAL', 'Annuel'),
        ('CUSTOM', 'Personnalisé'),
    ]
    FORMAT_CHOICES = [
        ('PDF', 'PDF Luxe'),
        ('EXCEL', 'Excel (Data)'),
    ]
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    file_path = models.CharField(max_length=255)
    stations_included = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Rapport {self.report_type} ({self.format}) - {self.created_at.strftime('%d/%m/%Y')}"
