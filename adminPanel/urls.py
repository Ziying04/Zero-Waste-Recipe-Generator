from django.urls import path
from .views import admin_dashboard, admin_user, admin_content, delete_user, admin_issues
from .views import (
    admin_dashboard, admin_user, delete_user, admin_content,
    delete_recipe, delete_donation, edit_recipe, edit_donation,
    recipe_detail_json, issue_detail, delete_issue, resolve_issue  # <-- added resolve_issue import
)

app_name = "adminPanel"

urlpatterns = [
    # Admin Dashboard and User Management Paths
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('admin-users/', admin_user, name='admin_user'),
    path('admin/users/<int:user_id>/delete/', delete_user, name='admin_delete_user'),
    path('admin-issues/', admin_issues, name='admin_issues'),  # List all issues
    path('issues/<int:issue_id>/', issue_detail, name='issue_detail'), 
    path('admin/issues/<int:issue_id>/resolve/', resolve_issue, name='resolve_issue'),  # Resolve specific issue
    path('admin/issues/<int:issue_id>/delete/', delete_issue, name='delete_issue'),  # Delete specific issue
    path('admin-content/recipe/<int:recipe_id>/delete/', delete_recipe, name='delete_recipe'),
    path('admin-content/donation/<int:donation_id>/delete/', delete_donation, name='delete_donation'),
    path('admin-content/recipe/<int:recipe_id>/edit/', edit_recipe, name='edit_recipe'),
    path('admin-content/donation/<int:donation_id>/edit/', edit_donation, name='edit_donation'),

    # New Paths for Managing Content (Approve, Hide, Delete Actions)
    # path('admin-content/approve/<int:content_id>/<str:content_type>/', approve_content, name='approve_content'),
    #path('admin-content/hide/<int:content_id>/<str:content_type>/', hide_content, name='hide_content'),
    #path('admin-content/delete/<int:content_id>/<str:content_type>/', delete_content, name='delete_content'),

    # Manage Content Path# Add other paths as needed
    #path('manage-content/', manage_content, name='manage_content'),  # Added manage_content path

    path('admin-content/recipe/<int:recipe_id>/json/', recipe_detail_json, name='recipe_detail_json'),
    path('admin-content/', admin_content, name='admin_content'),
    # Add other paths as needed
]

