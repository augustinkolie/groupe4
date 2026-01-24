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

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de réception")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    replied = models.BooleanField(default=False, verbose_name="Répondu")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.name} - {self.subject}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Abonné Newsletter"
        verbose_name_plural = "Abonnés Newsletter"

    def __str__(self):
        return self.email
