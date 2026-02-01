import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Station, Reading

def analyze_pollution_causes(station):
    """Analyse les données réelles de pollution et génère des causes contextuelles"""
    latest = station.readings.order_by('-timestamp').first()
    if not latest:
        return "<p>Données en cours de collecte...</p>"
    
    html = f'<div class="pollution-analysis"><div class="analysis-header"><strong>Dernière mesure:</strong> IQA {latest.iqa} | {latest.timestamp.strftime("%d/%m/%Y %H:%M")}</div><ul class="pollution-list">'
    
    # Analyser PM2.5
    if latest.pm25:
        level = "critique" if latest.pm25 > 35 else "modéré" if latest.pm25 > 12 else "bon"
        color = "#ef4444" if latest.pm25 > 35 else "#f59e0b" if latest.pm25 > 12 else "#10b981"
        sources = "trafic routier, combustion biomasse, poussières" if latest.pm25 > 35 else "circulation automobile, cuisson domestique" if latest.pm25 > 12 else "zone bien ventilée"
        html += f'<li><span class="pollutant-badge" style="background:{color}">PM2.5</span><strong>{latest.pm25:.1f} µg/m³</strong> - Niveau {level}<br><small>{sources}</small></li>'
    
    # Analyser CO
    if latest.co:
        level = "très élevé" if latest.co > 200 else "élevé" if latest.co > 100 else "acceptable"
        color = "#ef4444" if latest.co > 200 else "#f59e0b" if latest.co > 100 else "#10b981"
        sources = "véhicules anciens, groupes électrogènes, feux de brousse" if latest.co > 200 else "trafic dense, combustion domestique" if latest.co > 100 else "sources limitées"
        html += f'<li><span class="pollutant-badge" style="background:{color}">CO</span><strong>{latest.co:.1f} mg/m³</strong> - Niveau {level}<br><small>{sources}</small></li>'
    
    # Analyser NO2
    if latest.no2 and latest.no2 > 1:
        level = "élevé" if latest.no2 > 40 else "modéré"
        color = "#ef4444" if latest.no2 > 40 else "#f59e0b"
        html += f'<li><span class="pollutant-badge" style="background:{color}">NO₂</span><strong>{latest.no2:.1f} µg/m³</strong> - {level}<br><small>Émissions véhicules, industries</small></li>'
    
    # Analyser O3
    if latest.o3 and latest.o3 > 60:
        html += f'<li><span class="pollutant-badge" style="background:#f59e0b">O₃</span><strong>{latest.o3:.1f} µg/m³</strong> - Élevé<br><small>Pollution secondaire (rayonnement solaire)</small></li>'
    
    # Analyser SO2
    if latest.so2 and latest.so2 > 20:
        html += f'<li><span class="pollutant-badge" style="background:#ef4444">SO₂</span><strong>{latest.so2:.1f} µg/m³</strong> - Détecté<br><small>Industries, générateurs diesel</small></li>'
    
    html += '</ul></div>'
    return html

print("Analyse des données réelles de pollution et mise à jour...\n")
print("=" * 80)

for station in Station.objects.all():
    causes = analyze_pollution_causes(station)
    station.pollution_causes = causes
    station.save()
    print(f"\n✅ {station.name}")
    print(f"{causes}\n")
    print("-" * 80)

print("\n✅ Mise à jour terminée avec données réelles !")
