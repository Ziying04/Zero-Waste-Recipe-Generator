from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.db.models import Q

@login_required
def index(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notification.html', {
        'notifications': notifications
    })

@login_required
def get_notifications(request):
    """API to get user's notifications"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    result = []
    
    for notification in notifications:
        result.append({
            'id': notification.id,
            'type': notification.notification_type,
            'content': notification.content,
            'link': notification.link,
            'is_read': notification.is_read,
            'created_at': notification.created_at.strftime("%b %d, %Y, %I:%M %p")
        })
    
    return JsonResponse({
        'notifications': result,
        'unread_count': Notification.objects.filter(user=request.user, is_read=False).count()
    })

@login_required
def mark_as_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('notification-home')

@login_required
def mark_all_as_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('notification-home')
