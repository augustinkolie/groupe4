"""
Script complet de diagnostic et correction du système de génération PDF
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Reading, Station
from datetime import datetime, date, timedelta
import io

print("=" * 80)
print("DIAGNOSTIC ET TEST COMPLET DU SYSTÈME PDF")
print("=" * 80)

# 1. Vérifier les données
print("\n1️⃣ VÉRIFICATION DES DONNÉES")
print("-" * 80)

stations = Station.objects.all()
print(f"Stations disponibles: {stations.count()}")

end_date = date.today()
start_date = end_date - timedelta(days=7)

print(f"\nPériode: {start_date} → {end_date}")

for station in stations:
    count = Reading.objects.filter(
        station=station,
        timestamp__date__gte=start_date,
        timestamp__date__lte=end_date
    ).count()
    print(f"  {station.name}: {count} lectures")

# 2. Tester la génération PDF manuellement
print("\n2️⃣ TEST DE GÉNÉRATION PDF (MÉTHODE MANUELLE)")
print("-" * 80)

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER
    
    # Créer un buffer
    buffer = io.BytesIO()
    
    # Créer le document
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Titre
    title = Paragraph("<b>Rapport de Test EcoWatch</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 30))
    
    # Informations
    info = Paragraph(f"Période: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}", styles['Normal'])
    story.append(info)
    story.append(Spacer(1, 20))
    
    # Pour chaque station
    for station in stations:
        readings = Reading.objects.filter(
            station=station,
            timestamp__date__gte=start_date,
            timestamp__date__lte=end_date
        )
        
        if readings.exists():
            # Titre station
            station_title = Paragraph(f"<b>{station.name}</b>", styles['Heading2'])
            story.append(station_title)
            story.append(Spacer(1, 10))
            
            # Tableau de données
            from django.db.models import Avg, Max, Min
            stats = readings.aggregate(
                avg_iqa=Avg('iqa'),
                max_iqa=Max('iqa'),
                min_iqa=Min('iqa')
            )
            
            data = [
                ['Indicateur', 'Valeur'],
                ['IQA Moyen', f"{stats['avg_iqa']:.1f}" if stats['avg_iqa'] else 'N/A'],
                ['IQA Maximum', f"{stats['max_iqa']:.1f}" if stats['max_iqa'] else 'N/A'],
                ['IQA Minimum', f"{stats['min_iqa']:.1f}" if stats['min_iqa'] else 'N/A'],
                ['Nombre de relevés', str(readings.count())],
            ]
            
            table = Table(data, colWidths=[3*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            
            story.append(table)
            story.append(Spacer(1, 20))
    
    # Construire le PDF
    doc.build(story)
    
    # Vérifier le buffer
    pdf_data = buffer.getvalue()
    pdf_size = len(pdf_data)
    
    print(f"✅ PDF généré avec succès!")
    print(f"   Taille: {pdf_size} octets ({pdf_size / 1024:.2f} KB)")
    
    # Vérifier que c'est un PDF valide
    if pdf_data[:4] == b'%PDF':
        print(f"✅ En-tête PDF valide détecté")
    else:
        print(f"❌ En-tête PDF invalide!")
    
    # Sauvegarder
    test_file = "test_manuel_rapport.pdf"
    with open(test_file, 'wb') as f:
        f.write(pdf_data)
    
    print(f"📁 Sauvegardé: {os.path.abspath(test_file)}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

# 3. Tester avec le ReportGenerator
print("\n3️⃣ TEST AVEC REPORTGENERATOR")
print("-" * 80)

try:
    from monitoring.report_generator import ReportGenerator
    
    generator = ReportGenerator(stations, start_date, end_date, 'CUSTOM')
    pdf_buffer = generator.generate_pdf("test.pdf")
    
    pdf_data = pdf_buffer.getvalue()
    pdf_size = len(pdf_data)
    
    print(f"✅ ReportGenerator OK!")
    print(f"   Taille: {pdf_size} octets ({pdf_size / 1024:.2f} KB)")
    
    # Vérifier l'en-tête
    if pdf_data[:4] == b'%PDF':
        print(f"✅ PDF valide")
    else:
        print(f"❌ PDF invalide!")
        print(f"   Premiers octets: {pdf_data[:20]}")
    
    # Sauvegarder
    test_file2 = "test_generator_rapport.pdf"
    with open(test_file2, 'wb') as f:
        f.write(pdf_data)
    
    print(f"📁 Sauvegardé: {os.path.abspath(test_file2)}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

# 4. Simuler une requête HTTP
print("\n4️⃣ SIMULATION REQUÊTE HTTP")
print("-" * 80)

try:
    from django.test import RequestFactory
    from django.contrib.auth.models import AnonymousUser
    from monitoring.views import generate_report
    
    factory = RequestFactory()
    
    # Créer une requête POST simulée
    post_data = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'stations': [str(s.id) for s in stations],
        'report_type': 'CUSTOM'
    }
    
    request = factory.post('/reports/generate/', data=post_data)
    request.user = AnonymousUser()
    
    print(f"Données POST:")
    for key, value in post_data.items():
        print(f"  {key}: {value}")
    
    # Appeler la vue
    response = generate_report(request)
    
    print(f"\nRéponse HTTP:")
    print(f"  Status: {response.status_code}")
    print(f"  Content-Type: {response.get('Content-Type')}")
    
    if response.status_code == 200:
        content = response.content
        print(f"  Taille contenu: {len(content)} octets ({len(content) / 1024:.2f} KB)")
        
        if content[:4] == b'%PDF':
            print(f"✅ PDF valide dans la réponse!")
            
            # Sauvegarder
            test_file3 = "test_http_rapport.pdf"
            with open(test_file3, 'wb') as f:
                f.write(content)
            
            print(f"📁 Sauvegardé: {os.path.abspath(test_file3)}")
        else:
            print(f"❌ Contenu invalide!")
            print(f"   Premiers octets: {content[:50]}")
    else:
        print(f"❌ Erreur HTTP {response.status_code}")
        
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("RÉSUMÉ")
print("=" * 80)
print("\n✅ Si tous les tests sont passés, vérifiez les 3 fichiers PDF générés:")
print("   1. test_manuel_rapport.pdf")
print("   2. test_generator_rapport.pdf")
print("   3. test_http_rapport.pdf")
print("\n💡 Ouvrez-les pour confirmer qu'ils contiennent bien les données!")
print("=" * 80)
