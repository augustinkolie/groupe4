from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from monitoring.models import Station, Reading
from .forms import StationForm
from .ai_service import AIService

ai_service = AIService()

def stats_overview(request):
    """
    Returns the HTML partial for dashboard statistics.
    Uses last 24 hours for rolling statistics.
    """
    time_threshold = timezone.now() - timedelta(hours=24)
    
    total_stations = Station.objects.count()
    readings_24h = Reading.objects.filter(timestamp__gte=time_threshold).count()
    
    # Calculate average AQI from readings in last 24h
    avg_iqa = Reading.objects.filter(timestamp__gte=time_threshold).aggregate(Avg('iqa'))['iqa__avg'] or 0
    
    context = {
        'total_stations': total_stations,
        'readings_today': readings_24h,
        'avg_iqa': round(avg_iqa),
        'alerts_count': 0, 
        'last_sync': timezone.now(),
    }
    return render(request, 'monitoring/partials/stats_overview.html', context)

def trigger_api_fetch(request):
    """
    Optional view to trigger an API fetch and then return updated stats.
    """
    from ingestion.management.commands.fetch_air_quality import Command
    cmd = Command()
    cmd.handle() # Fetch real data
    return stats_overview(request)

def map_sync_badge(request):
    """
    Returns the HTML partial for the map synchronization badge.
    """
    context = {
        'current_time': timezone.now(),
    }
    return render(request, 'monitoring/partials/map_sync_badge.html', context)

def station_details_partial(request, station_id):
    """
    Returns the HTML partial for station details (grid of stats).
    """
    try:
        station = Station.objects.get(id=station_id)
        latest = station.readings.first()
        
        context = {
            'station': station,
            'latest': latest,
        }
        return render(request, 'monitoring/partials/station_details.html', context)
    except Station.DoesNotExist:
        return render(request, 'monitoring/partials/station_details.html', {'error': 'Station introuvable'})

def station_popup_partial(request, station_id):
    """
    Returns the HTML partial for station popup (marker info).
    """
    try:
        station = Station.objects.get(id=station_id)
        latest = station.readings.first()
        
        context = {
            'station': station,
            'latest': latest,
        }
        return render(request, 'monitoring/partials/station_popup.html', context)
    except Station.DoesNotExist:
        return HttpResponse('<div>Station introuvable</div>')

def get_station_edit_form(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    form = StationForm(instance=station)
    return render(request, 'monitoring/partials/edit_station_form.html', {
        'station': station,
        'station_form': form,
    })

import uuid

def chatbot_query(request):
    """
    Handles chatbot messages via HTMX.
    """
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        if not user_message:
            return HttpResponse('')
            
        # 1. ANALYSE TRENDS (Dernières 24h)
        time_threshold = timezone.now() - timedelta(hours=24)
        
        # Aggregate returns None if no data, ensure 0
        agg_pm25 = Reading.objects.filter(timestamp__gte=time_threshold).aggregate(Avg('pm25'))['pm25__avg']
        avg_pm25 = round(agg_pm25) if agg_pm25 is not None else 0
        
        agg_temp = Reading.objects.filter(timestamp__gte=time_threshold).aggregate(Avg('temperature'))['temperature__avg']
        avg_temp = round(agg_temp) if agg_temp is not None else 0
        
        trends_summary = f"Moyenne 24h: PM2.5={avg_pm25}µg/m³, Temp={avg_temp}°C"

        # 2. CONTEXTE TEMPS RÉEL
        recent_readings = Reading.objects.order_by('-timestamp')[:5]
        realtime_data = "\n".join([str(r) for r in recent_readings])
        
        full_context = f"TENDANCES 24H: {trends_summary}\n\nDONNÉES TEMPS RÉEL:\n{realtime_data}"
        
        # 3. GESTION MÉMOIRE (Session)
        history = request.session.get('chat_history', [])
        
        # Appel IA avec historique
        try:
            response_text = ai_service.get_chat_response(user_message, context=full_context, history=history)
        except Exception as e:
            response_text = "Désolé, je rencontre une erreur de connexion à mon cerveau IA. 🧠⚠️"
        
        # Mise à jour historique (User + AI)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": response_text})
        
        # Limiter à 10 échanges pour préserver la session
        request.session['chat_history'] = history[-10:]
        
        # ID unique pour le script JS
        message_id = f"msg-{str(uuid.uuid4())[:8]}"
        
        return render(request, 'monitoring/partials/chatbot_message.html', {
            'user_message': user_message,
            'response_text': response_text,
            'message_id': message_id,
        })

def station_ai_insights(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    recent_readings = Reading.objects.filter(station=station).order_by('-timestamp')[:10]
    
    if not recent_readings.exists():
        return HttpResponse('<div class="ai-insight-card">Aucune donnée disponible pour analyse.</div>')
        
    # Format data for AI
    data_summary = "\n".join([
        f"{r.timestamp.strftime('%H:%M')}: IQA={r.iqa}, PM2.5={r.pm25}, Temp={r.temperature}°C"
        for r in recent_readings
    ])
    
    analysis = ai_service.analyze_readings(f"Station {station.name}:\n{data_summary}")
    
    return render(request, 'monitoring/partials/station_ai_insights.html', {
        'station': station,
        'analysis': analysis
    })

