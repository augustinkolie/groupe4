from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm, ContactForm, NewsletterForm
from datetime import timedelta
from rest_framework import viewsets
from django.utils import timezone
from .models import Station, Reading
from .serializers import StationSerializer, ReadingSerializer

def index(request):
    stations = Station.objects.all()
    return render(request, 'monitoring/index.html', {'stations': stations})

def dashboard(request):
    return render(request, 'monitoring/dashboard.html')

def contact(request):
    contact_form = ContactForm()
    newsletter_form = NewsletterForm()

    if request.method == 'POST':
        if 'submit_contact' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, 'Votre message a été envoyé avec succès !')
                return redirect('contact')
            else:
                 messages.error(request, 'Une erreur est survenue, veuillez vérifier le formulaire.')
        elif 'submit_newsletter' in request.POST:
            newsletter_form = NewsletterForm(request.POST)
            if newsletter_form.is_valid():
                newsletter_form.save()
                messages.success(request, 'Merci de votre inscription à la newsletter !')
                return redirect('contact')

    context = {
        'form': contact_form,
        'newsletter_form': newsletter_form
    }
    return render(request, 'monitoring/contact.html', context)

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
