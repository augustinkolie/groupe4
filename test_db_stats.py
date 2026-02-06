import os
import django
import sys
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDay

# Configuration de l'environnement Django
sys.path.append('d:\\Projet_Python\\groupe4')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import AlertLog, Station, Reading

def verify_db_stats():
    print("--- Vérification de la liaison Base de Données ---")
    
    # 1. Vérification du nombre total
    total = AlertLog.objects.count()
    print(f"Total des alertes en base : {total}")

    # 2. Test Agrégation par Station
    print("\nRépartition par Station (SQL Query):")
    stats_station = AlertLog.objects.values('station__name').annotate(count=Count('id')).order_by('-count')
    for stat in stats_station:
        print(f" - {stat['station__name']}: {stat['count']} alertes")

    # 3. Test Fréquence Temporelle
    print("\nFréquence Temporelle (30 derniers jours):")
    month_threshold = timezone.now() - timedelta(days=30)
    stats_day = AlertLog.objects.filter(created_at__gte=month_threshold)\
        .annotate(day=TruncDay('created_at'))\
        .values('day')\
        .annotate(count=Count('id'))\
        .order_by('day')
    
    for stat in stats_day:
        print(f" - {stat['day'].strftime('%d/%m/%Y')}: {stat['count']} alertes")

    if total > 0:
        print("\n✅ SUCCÈS : Les données sont bien extraites dynamiquement de la base de données.")
    else:
        print("\nℹ️ NOTE : La base est vide, mais les requêtes SQL sont prêtes et fonctionnelles.")

if __name__ == "__main__":
    verify_db_stats()
