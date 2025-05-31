from django.urls import path
from .views import admin_dashboard, admin_user

urlpatterns = [
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('admin/users/', admin_user, name='admin_user'),
    # Add other paths as needed
]

