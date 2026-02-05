from .models import AlertRule, AlertLog
from django.utils import timezone

def check_alert_rules(reading):
    """
    Vérifie les règles d'alerte pour une nouvelle lecture.
    Crée des AlertLog si nécessaire.
    """
    rules = AlertRule.objects.filter(is_active=True)
    
    triggered = False
    
    for rule in rules:
        violation_msg = []
        
        # Vérification des seuils
        if rule.iqa_threshold and reading.iqa and reading.iqa > rule.iqa_threshold:
            violation_msg.append(f"IQA {reading.iqa} > {rule.iqa_threshold}")
            
        if rule.pm25_threshold and reading.pm25 and reading.pm25 > rule.pm25_threshold:
            violation_msg.append(f"PM2.5 {reading.pm25} > {rule.pm25_threshold}")
            
        if rule.co_threshold and reading.co and reading.co > rule.co_threshold:
            violation_msg.append(f"CO {reading.co} > {rule.co_threshold}")
            
        if rule.temperature_threshold and reading.temperature and reading.temperature > rule.temperature_threshold:
            violation_msg.append(f"Temp {reading.temperature} > {rule.temperature_threshold}")
            
        if violation_msg:
            # Créer une alerte
            full_msg = ", ".join(violation_msg)
            
            # Éviter doublon pour ce reading/rule
            if not AlertLog.objects.filter(reading=reading, rule=rule).exists():
                AlertLog.objects.create(
                    station=reading.station,
                    rule=rule,
                    reading=reading,
                    message=f"Seuils dépassés: {full_msg}",
                    is_resolved=False
                )
                triggered = True
                
                # Simulation notification
                print(f"🚨 ALERTE DÉCLENCHÉE [{reading.station.name}]: {full_msg}")
                if rule.email_notification and rule.email_address:
                    print(f"   📧 Envoi email à {rule.email_address}...")
                if rule.sms_notification and rule.phone_number:
                    print(f"   📱 Envoi SMS à {rule.phone_number}...")

    return triggered
