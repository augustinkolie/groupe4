from .models import AlertLog, ContactMessage

def notifications_context(request):
    """
    Context processor pour fournir les compteurs de notifications globalement.
    """
    if not request.user.is_authenticated:
        return {
            'unread_notifications_count': 0,
            'unread_alerts_count': 0,
            'unread_messages_count': 0,
        }
    
    try:
        unread_alerts = AlertLog.objects.filter(is_read=False).count()
        unread_messages = ContactMessage.objects.filter(is_read=False).count()
        
        return {
            'unread_notifications_count': unread_alerts + unread_messages,
            'unread_alerts_count': unread_alerts,
            'unread_messages_count': unread_messages,
        }
    except Exception:
        return {
            'unread_notifications_count': 0,
            'unread_alerts_count': 0,
            'unread_messages_count': 0,
        }
