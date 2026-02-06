import os
import django
import sys
import random
from django.utils import timezone
from datetime import timedelta

# Configuration environment
sys.path.append('d:\\Projet_Python\\groupe4')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import AlertLog, Station, AlertRule, Reading

def seed_mock_alerts():
    print("🚀 Génération de données de démonstration...")
    
    stations = Station.objects.all()
    if not stations.exists():
        print("❌ Aucune station trouvée. Abandon.")
        return

    rule, _ = AlertRule.objects.get_or_create(id=1)

    # Messages types
    messages = [
        "Dépassement critique du seuil IQA",
        "Niveau de PM2.5 dangereux détecté",
        "Alerte : Forte concentration de CO",
        "Température anormale enregistrée"
    ]

    # Création de 50 alertes aléatoires sur 30 jours
    now = timezone.now()
    created_count = 0
    
    for _ in range(50):
        # Date aléatoire dans les 30 derniers jours
        random_days = random.randint(0, 30)
        random_hours = random.randint(0, 23)
        alert_time = now - timedelta(days=random_days, hours=random_hours)
        
        station = random.choice(stations)
        msg = random.choice(messages)
        
        # Création d'une lecture fictive pour l'alerte
        reading = Reading.objects.create(
            station=station,
            timestamp=alert_time,
            iqa=random.randint(101, 200),
            source_type='SENSOR'
        )
        
        alert = AlertLog.objects.create(
            station=station,
            rule=rule,
            reading=reading,
            message=f"[DEMO] {msg}",
            is_resolved=random.choice([True, False])
        )
        # Force created_at
        AlertLog.objects.filter(id=alert.id).update(created_at=alert_time)
        created_count += 1

    print(f"✅ {created_count} alertes de démonstration générées avec succès.")

if __name__ == "__main__":
    seed_mock_alerts()
