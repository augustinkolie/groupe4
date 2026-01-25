from django.shortcuts import render
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from monitoring.models import Station, Reading

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
