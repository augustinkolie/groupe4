import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station, Reading, AlertRule, AlertLog
from monitoring.utils import check_alert_rules
from django.utils import timezone

def test_alerts():
    print("🚀 Test du système d'alertes...")
    
    # 1. Configurer une règle (IQA > 100)
    rule, _ = AlertRule.objects.get_or_create(id=1)
    rule.iqa_threshold = 100
    rule.is_active = True
    rule.save()
    print(f"✅ Règle configurée: IQA > {rule.iqa_threshold}")
    
    # 2. Créer une station de test
    station = Station.objects.first()
    if not station:
        print("❌ Aucune station trouvée pour le test.")
        return

    # 3. Créer un relevé qui dépasse le seuil
    print(f"📡 Simulation d'un relevé pollué pour {station.name}...")
    reading = Reading.objects.create(
        station=station,
        timestamp=timezone.now(),
        iqa=150,
        pm25=75.0,
        source_type='SENSOR',
        source_id='test_device'
    )
    
    # 4. Déclencher la vérification
    triggered = check_alert_rules(reading)
    
    if triggered:
        print("✅ Alerte DÉCLENCHÉE avec succès !")
        latest_log = AlertLog.objects.filter(reading=reading).first()
        if latest_log:
            print(f"📝 Message d'alerte: {latest_log.message}")
        else:
            print("❌ Erreur: Pas de log trouvé.")
    else:
        print("❌ Échec: L'alerte n'a pas été déclenchée.")

if __name__ == "__main__":
    test_alerts()
