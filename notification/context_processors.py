from .models import Notification

def notification_count(request):
    """Return the unread notification count for the current user"""
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'notifications_unread_count': unread_count}
    return {'notifications_unread_count': 0}
