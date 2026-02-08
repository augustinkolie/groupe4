from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncDay
from .forms import CustomUserCreationForm, ContactForm, NewsletterForm, StationForm
from datetime import timedelta, datetime
from rest_framework import viewsets
from django.utils import timezone
from .models import Station, Reading, AlertRule, AlertLog, GeneratedReport
from .serializers import StationSerializer, ReadingSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import LineChart, Reference
from .report_generator import ReportGenerator
import os
from django.conf import settings

def index(request):
    stations = Station.objects.all()
    return render(request, 'monitoring/index.html', {'stations': stations})

def dashboard(request):
    return render(request, 'monitoring/dashboard.html')

def contact(request):
    form = ContactForm()
    newsletter_form = NewsletterForm()

    if request.method == 'POST':
        if 'submit_contact' in request.POST:
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Votre message a été envoyé avec succès !")
                return redirect('contact')
        
        elif 'submit_newsletter' in request.POST:
            newsletter_form = NewsletterForm(request.POST)
            if newsletter_form.is_valid():
                newsletter_form.save()
                messages.success(request, "Merci de vous être inscrit à notre newsletter !")
                return redirect('contact')
            else:
                messages.error(request, "Une erreur est survenue lors de l'inscription à la newsletter.")

    context = {
        'form': form,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'monitoring/contact.html', context)

def features(request):
    return render(request, 'monitoring/features.html')

def about(request):
    return render(request, 'monitoring/about.html')

from django.core.paginator import Paginator

def stations_list(request):
    stations_list = Station.objects.all().order_by('-created_at')
    paginator = Paginator(stations_list, 6) # Show 6 stations per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'monitoring/stations.html', {
        'page_obj': page_obj,
        'station_form': StationForm()
    })

def add_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST, request.FILES)
        if form.is_valid():
            station = form.save()
            if request.headers.get('HX-Request'):
                messages.success(request, f"La station {station.name} a été ajoutée avec succès !")
                return HttpResponse(status=204, headers={'HX-Trigger': 'stationAdded'})
            
            messages.success(request, f"La station {station.name} a été ajoutée avec succès !")
            return redirect('stations')
    
    return redirect('stations')

def edit_station(request, pk):
    station = get_object_or_404(Station, pk=pk)
    if request.method == 'POST':
        form = StationForm(request.POST, request.FILES, instance=station)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                messages.success(request, f"La station {station.name} a été modifiée avec succès !")
                return HttpResponse(status=204, headers={'HX-Trigger': 'stationUpdated'})
            
            messages.success(request, f"La station {station.name} a été modifiée avec succès !")
            return redirect('stations')
    
    return redirect('stations')

@require_http_methods(['DELETE', 'POST'])
def delete_station(request, pk):
    station = get_object_or_404(Station, pk=pk)
    station_name = station.name
    station.delete()
    
    if request.headers.get('HX-Request'):
        messages.success(request, f"La station {station_name} a été supprimée.")
        return HttpResponse(status=204, headers={'HX-Trigger': 'stationDeleted'})
    
    messages.success(request, f"La station {station_name} a été supprimée.")
    return redirect('stations')

def alerts_view(request):
    # Récupérer la règle d'alerte globale (pour l'exemple)
    rule, created = AlertRule.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        # Mise à jour des seuils
        rule.iqa_threshold = request.POST.get('iqa_threshold') or None
        rule.pm25_threshold = request.POST.get('pm25_threshold') or None
        rule.co_threshold = request.POST.get('co_threshold') or None
        rule.temperature_threshold = request.POST.get('temp_threshold') or None
        
        # Notifications
        rule.email_address = request.POST.get('email')
        rule.phone_number = request.POST.get('phone')
        rule.email_notification = 'email_notif' in request.POST
        rule.sms_notification = 'sms_notif' in request.POST
        
        rule.save()
        messages.success(request, "Configuration des alertes mise à jour.")
        return redirect('alerts')

    time_threshold = timezone.now() - timedelta(hours=24)
    month_threshold = timezone.now() - timedelta(days=30)
    
    # Statistiques réelles
    alerts_all = AlertLog.objects.all().order_by('-created_at')
    alerts_today_count = alerts_all.filter(created_at__gte=time_threshold).count()
    
    # Répartition par station
    alerts_by_station = list(AlertLog.objects.values('station__name').annotate(count=Count('id')).order_by('-count'))
    
    # Filière temporelle (30 derniers jours)
    alerts_by_day = AlertLog.objects.filter(created_at__gte=month_threshold)\
        .annotate(day=TruncDay('created_at'))\
        .values('day')\
        .annotate(count=Count('id'))\
        .order_by('day')
    
    # Formater pour Chart.js
    alerts_by_day_list = [
        {'day': item['day'].strftime('%d/%m'), 'count': item['count']}
        for item in alerts_by_day
    ]

    context = {
        'rule': rule,
        'alerts': alerts_all[:10], # 10 dernières alertes
        'alerts_total': alerts_all.count(),
        'alerts_today': alerts_today_count,
        'rules_count': 1,
        'alerts_by_station': alerts_by_station,
        'alerts_by_day': alerts_by_day_list,
    }
    return render(request, 'monitoring/alerts.html', context)

def reports_view(request):
    stations = Station.objects.all()
    total_readings = Reading.objects.all().count()
    
    # Récupérer l'historique réel des rapports
    generated_reports = GeneratedReport.objects.all()[:10]  # 10 derniers rapports
    total_reports = GeneratedReport.objects.count()
    total_exports = GeneratedReport.objects.filter(created_at__month=timezone.now().month).count()
    
    context = {
        'stations': stations,
        'total_reports': total_reports,
        'total_exports': total_exports,
        'total_readings': total_readings,
        'generated_reports': generated_reports,
    }
    return render(request, 'monitoring/reports.html', context)

def exports_view(request):
    """Centre de téléchargement des rapports et exports archivés"""
    exports = GeneratedReport.objects.all().order_by('-created_at')
    return render(request, 'monitoring/exports.html', {'exports': exports})

def analyses_view(request):
    return render(request, 'monitoring/analyses.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer

    def get_queryset(self):
        queryset = Reading.objects.all()
        station_id = self.request.query_params.get('station')
        if station_id:
            queryset = queryset.filter(station_id=station_id)
        return queryset

    def perform_create(self, serializer):
        # Optional: Add logic to calculate IQA if not provided by the sensor
        instance = serializer.save()
        if not instance.iqa:
            # Simple placeholder logic for IQA calculation
            # Based on PM2.5 (very simplified for now)
            instance.iqa = int(instance.pm25 * 2) if instance.pm25 else 0
            instance.save()
        
        # Déclenchement des alertes pour les capteurs physiques également
        from .utils import check_alert_rules
        check_alert_rules(instance)

@require_POST
def generate_report(request):
    """Génère un rapport PDF"""
    try:
        # Récupérer les paramètres
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        station_ids = request.POST.getlist('stations')
        report_type = request.POST.get('report_type', 'CUSTOM')
        
        # Debug logs to file
        with open('debug_pdf.log', 'a', encoding='utf-8') as log:
            log.write(f"\n--- {datetime.now()} ---\n")
            log.write(f"Parameters: start={start_date_str}, end={end_date_str}, stations={station_ids}\n")
        
        if not start_date_str or not end_date_str or not station_ids:
            return JsonResponse({'error': 'Paramètres manquants'}, status=400)

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Récupérer les stations
        stations = Station.objects.filter(id__in=station_ids)
        if not stations.exists():
            return JsonResponse({'error': 'Aucune station trouvée'}, status=400)
        
        # Vérifier les données disponibles
        total_readings = 0
        for station in stations:
            count = Reading.objects.filter(
                station=station,
                timestamp__date__gte=start_date,
                timestamp__date__lte=end_date
            ).count()
            total_readings += count
        
        with open('debug_pdf.log', 'a', encoding='utf-8') as log:
            log.write(f"Total readings found in DB: {total_readings}\n")
            
        if total_readings == 0:
            return JsonResponse({'error': 'Aucune donnée trouvée pour cette période et ces stations'}, status=400)
            
        # Générer le rapport
        report_format = request.POST.get('format', 'PDF')
        generator = ReportGenerator(stations, start_date, end_date, report_type)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if report_format == 'EXCEL':
            filename = f"rapport_ecowatch_{timestamp}.xlsx"
            report_buffer = generator.generate_excel(filename)
        else:
            filename = f"rapport_ecowatch_{timestamp}.pdf"
            report_buffer = generator.generate_pdf(filename)
        
        report_data = report_buffer.getvalue()
        
        with open('debug_pdf.log', 'a', encoding='utf-8') as log:
            log.write(f"Report ({report_format}) generated size: {len(report_data)} bytes\n")
            
        # Sauvegarder le fichier dans media/reports
        reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        file_path = os.path.join(reports_dir, filename)
        
        with open(file_path, 'wb') as f:
            f.write(report_data)
        
        # Créer un enregistrement dans la base de données
        GeneratedReport.objects.create(
            report_type=report_type,
            format=report_format,
            start_date=start_date,
            end_date=end_date,
            file_path=f'reports/{filename}',
            stations_included=[{'id': s.id, 'name': s.name} for s in stations]
        )
        
        # Retourner l'URL du fichier en JSON pour un téléchargement propre côté client
        return JsonResponse({
            'success': True,
            'url': f"{settings.MEDIA_URL}reports/{filename}",
            'filename': filename
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        stack_trace = traceback.format_exc()
        
        with open('debug_pdf.log', 'a', encoding='utf-8') as log:
            log.write(f"❌ CRASH: {error_msg}\n")
            log.write(f"{stack_trace}\n")
            
        print(f"   ❌ ERREUR: {error_msg}")
        return JsonResponse({'error': error_msg}, status=500)

@require_POST
def export_excel(request):
    """Exporte les données vers Excel"""
    try:
        # Paramètres optionnels pour export rapide
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        station_ids = request.POST.getlist('stations')
        
        # Si pas de paramètres, exporter toutes les données récentes
        if not start_date_str or not end_date_str:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
            stations = Station.objects.all()
        else:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            stations = Station.objects.filter(id__in=station_ids) if station_ids else Station.objects.all()
        
        # Créer le workbook Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Données Qualité de l'Air"
        
        # En-têtes
        headers = ['Date/Heure', 'Station', 'IQA', 'PM2.5', 'PM10', 'CO', 'NO2', 'SO2', 'O3', 'Température', 'Humidité']
        ws.append(headers)
        
        # Style des en-têtes
        header_fill = PatternFill(start_color="10b981", end_color="10b981", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center')
        
        # Données
        for station in stations:
            readings = Reading.objects.filter(
                station=station,
                timestamp__date__gte=start_date,
                timestamp__date__lte=end_date
            ).order_by('timestamp')
            
            for reading in readings:
                ws.append([
                    reading.timestamp.strftime('%d/%m/%Y %H:%M'),
                    station.name,
                    reading.iqa or '',
                    reading.pm25 or '',
                    reading.pm10 or '',
                    reading.co or '',
                    reading.no2 or '',
                    reading.so2 or '',
                    reading.o3 or '',
                    reading.temperature or '',
                    reading.humidity or '',
                ])
        
        # Ajuster les largeurs de colonnes
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Sauvegarder dans un buffer
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="ecowatch_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
        wb.save(response)
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
def export_csv(request):
    """Exporte toutes les données vers CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="ecowatch_data_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date/Heure', 'Station', 'Latitude', 'Longitude', 'IQA', 'PM2.5', 'PM10', 'CO', 'NO2', 'SO2', 'O3', 'Température', 'Humidité', 'Source'])
    
    readings = Reading.objects.select_related('station').order_by('-timestamp')[:10000]  # Limiter à 10000 derniers relevés
    
    for reading in readings:
        writer.writerow([
            reading.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            reading.station.name,
            reading.station.latitude,
            reading.station.longitude,
            reading.iqa or '',
            reading.pm25 or '',
            reading.pm10 or '',
            reading.co or '',
            reading.no2 or '',
            reading.so2 or '',
            reading.o3 or '',
            reading.temperature or '',
            reading.humidity or '',
            reading.source_type,
        ])
    
    return response