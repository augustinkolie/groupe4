import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Reading, Station
from monitoring.report_generator import ReportGenerator
from datetime import datetime, date, timedelta

print("=" * 80)
print("TEST DE GÉNÉRATION PDF")
print("=" * 80)

# Dates de test
end_date = date.today()
start_date = end_date - timedelta(days=7)

print(f"\n📅 Période de test:")
print(f"   Du: {start_date.strftime('%d/%m/%Y')}")
print(f"   Au: {end_date.strftime('%d/%m/%Y')}")

# Récupérer toutes les stations
stations = Station.objects.all()
print(f"\n🏢 Stations sélectionnées: {stations.count()}")

# Vérifier les données pour chaque station
print(f"\n🔍 Vérification des données:")
for station in stations:
    readings = Reading.objects.filter(
        station=station,
        timestamp__date__gte=start_date,
        timestamp__date__lte=end_date
    )
    count = readings.count()
    print(f"   {station.name}: {count} lectures trouvées")
    
    if count > 0:
        latest = readings.order_by('-timestamp').first()
        print(f"      └─ Dernière: {latest.timestamp}, IQA: {latest.iqa}")

# Générer le PDF
print(f"\n📄 Génération du PDF...")
try:
    generator = ReportGenerator(stations, start_date, end_date, 'CUSTOM')
    pdf_buffer = generator.generate_pdf("test_report.pdf")
    
    # Vérifier la taille du buffer
    pdf_size = len(pdf_buffer.getvalue())
    print(f"   ✅ PDF généré avec succès!")
    print(f"   Taille: {pdf_size} octets ({pdf_size / 1024:.2f} KB)")
    
    # Sauvegarder pour inspection
    test_file = "test_rapport.pdf"
    with open(test_file, 'wb') as f:
        pdf_buffer.seek(0)
        f.write(pdf_buffer.read())
    
    print(f"   📁 Sauvegardé dans: {os.path.abspath(test_file)}")
    print(f"\n   💡 Ouvrez ce fichier pour vérifier le contenu!")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
