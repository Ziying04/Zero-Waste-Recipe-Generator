from django.urls import path
from .views import admin_dashboard, admin_user, admin_content

urlpatterns = [
    # path('admin/', admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard')
    path('admin-users/', admin_user, name='admin_user'),
    path('admin-content/', admin_content, name='admin_content'),
    # Add other paths as needed
]

