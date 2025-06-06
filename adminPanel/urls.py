# Add this to your urls.py
from django.urls import path
from .views import (
    admin_dashboard, admin_user, delete_user, admin_content, admin_issues,
    delete_recipe, delete_donation, edit_recipe, edit_donation,
    recipe_detail_json, donation_detail_json, issue_detail, delete_issue, resolve_issue,
    create_recipe, create_donation, debug_donation_model, create_user, add_user_view,  # Added add_user_view
)

app_name = "adminPanel"

urlpatterns = [
    # Admin Dashboard and User Management Paths
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('admin-users/', admin_user, name='admin_user'),
    path('admin/users/<int:user_id>/delete/', delete_user, name='admin_delete_user'),
    path('admin/users/create/', create_user, name='admin_create_user'),
    path('add-user/', add_user_view, name='add_user_view'),  # Simplified URL
    
    # Issues Management
    path('admin-issues/', admin_issues, name='admin_issues'),
    path('issues/<int:issue_id>/', issue_detail, name='issue_detail'), 
    path('admin/issues/<int:issue_id>/resolve/', resolve_issue, name='resolve_issue'),
    path('admin/issues/<int:issue_id>/delete/', delete_issue, name='delete_issue'),
    
    # Content Management
    path('admin-content/', admin_content, name='admin_content'),
    
    # Recipe Management
    path('admin-content/recipe/create/', create_recipe, name='create_recipe'),
    path('admin-content/recipe/<int:recipe_id>/edit/', edit_recipe, name='edit_recipe'),
    path('admin-content/recipe/<int:recipe_id>/delete/', delete_recipe, name='delete_recipe'),
    path('admin-content/recipe/<int:recipe_id>/json/', recipe_detail_json, name='recipe_detail_json'),
    
    # Donation Management  
    path('admin-content/donation/create/', create_donation, name='create_donation'),
    path('admin-content/donation/<int:donation_id>/edit/', edit_donation, name='edit_donation'),
    path('admin-content/donation/<int:donation_id>/delete/', delete_donation, name='delete_donation'),
    path('admin-content/donation/<int:donation_id>/json/', donation_detail_json, name='donation_detail_json'),  # Add this line
    path('debug/donation/<int:donation_id>/', debug_donation_model, name='debug_donation'),
]