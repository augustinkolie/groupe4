import os
import django
import sys

# Configuration environment
sys.path.append('d:\\Projet_Python\\groupe4')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import AlertLog, Reading

def cleanup_mock_alerts():
    print("🧹 Nettoyage des données de démonstration...")
    
    # On identifie les alertes par le tag [DEMO]
    demo_alerts = AlertLog.objects.filter(message__contains="[DEMO]")
    count = demo_alerts.count()
    
    # Supprimer aussi les lectures associées pour ne pas polluer les autres graphiques
    reading_ids = list(demo_alerts.values_list('reading_id', flat=True))
    
    demo_alerts.delete()
    Reading.objects.filter(id__in=reading_ids).delete()
    
    print(f"✅ {count} alertes et lectures de démonstration supprimées.")

if __name__ == "__main__":
    cleanup_mock_alerts()
