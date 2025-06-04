from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='notification-home'),
    path('api/get-notifications/', views.get_notifications, name='get-notifications'),
    path('mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark-as-read'),
    path('mark-all-as-read/', views.mark_all_as_read, name='mark-all-as-read'),
]
