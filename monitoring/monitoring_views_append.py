
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
