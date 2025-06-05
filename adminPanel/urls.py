from django.urls import path
from .views import admin_dashboard, admin_user, delete_user, admin_issues, resolve_issue, delete_issue, issue_detail

app_name = "adminPanel"

urlpatterns = [
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('admin-users/', admin_user, name='admin_user'),
    path('admin/users/<int:user_id>/delete/', delete_user, name='admin_delete_user'),
    path('admin-issues/', admin_issues, name='admin_issues'),  # List all issues
    path('issues/<int:issue_id>/', issue_detail, name='issue_detail'), 
    path('admin/issues/<int:issue_id>/resolve/', resolve_issue, name='resolve_issue'),  # Resolve specific issue
    path('admin/issues/<int:issue_id>/delete/', delete_issue, name='delete_issue'),  # Delete specific issue
    # Add other paths as needed
]

