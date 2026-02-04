from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm, ContactForm, NewsletterForm
from datetime import timedelta, datetime
from rest_framework import viewsets
from django.utils import timezone
from .models import Station, Reading
from .serializers import StationSerializer, ReadingSerializer
from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.http import require_POST
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import LineChart, Reference
from .report_generator import ReportGenerator
import os

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
    
    return render(request, 'monitoring/stations.html', {'page_obj': page_obj})

def alerts_view(request):
    time_threshold = timezone.now() - timedelta(hours=24)
    # Count readings with IQA > 100 as "alerts" for demonstration
    alerts_count = Reading.objects.filter(iqa__gt=100, timestamp__gte=time_threshold).count()
    context = {
        'alerts_total': alerts_count,
        'alerts_today': alerts_count, # Simplified
        'rules_count': 4, # Mock count
    }
    return render(request, 'monitoring/alerts.html', context)

def reports_view(request):
    stations = Station.objects.all()
    total_readings = Reading.objects.all().count()
    context = {
        'stations': stations,
        'total_reports': 12, # Mock count
        'total_exports': 45, # Mock count
        'total_readings': total_readings,
    }
    return render(request, 'monitoring/reports.html', context)

def exports_view(request):
    return render(request, 'monitoring/exports.html')

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
            instance.iqa = int(instance.pm25 * 2) 
            instance.save()

@require_POST
def generate_report(request):
    """Génère un rapport PDF"""
    try:
        # Récupérer les paramètres
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        station_ids = request.POST.getlist('stations')
        report_type = request.POST.get('report_type', 'CUSTOM')
        
        # Debug logs
        print(f"🔍 DEBUG - Génération rapport:")
        print(f"   start_date: {start_date_str}")
        print(f"   end_date: {end_date_str}")
        print(f"   station_ids: {station_ids}")
        print(f"   report_type: {report_type}")
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Récupérer les stations
        stations = Station.objects.filter(id__in=station_ids)
        
        if not stations.exists():
            print(f"   ❌ Aucune station trouvée!")
            return JsonResponse({'error': 'Aucune station sélectionnée'}, status=400)
        
        print(f"   ✅ {stations.count()} stations trouvées")
        
        # Vérifier les données disponibles
        total_readings = 0
        for station in stations:
            count = Reading.objects.filter(
                station=station,
                timestamp__date__gte=start_date,
                timestamp__date__lte=end_date
            ).count()
            print(f"   {station.name}: {count} lectures")
            total_readings += count
        
        print(f"   📊 Total lectures: {total_readings}")
        
        # Générer le rapport
        generator = ReportGenerator(stations, start_date, end_date, report_type)
        filename = f"rapport_ecowatch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_buffer = generator.generate_pdf(filename)
        
        # Vérifier la taille
        pdf_data = pdf_buffer.getvalue()
        pdf_size = len(pdf_data)
        print(f"   📄 PDF généré: {pdf_size} octets ({pdf_size / 1024:.2f} KB)")
        
        # Retourner le fichier
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = len(pdf_data)
        response['Cache-Control'] = 'no-cache'
        return response
        
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

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