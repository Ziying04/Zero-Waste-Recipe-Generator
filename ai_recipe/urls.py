"""
URL configuration for ai_recipe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Import directly from ai_recipe.views
from ai_recipe.views import IngredientSearchView, recipe_ai
from ai_recipe.views import home, custom_login, admin_dashboard, admin_user, admin_content, custom_logout, custom_signup

urlpatterns = [
    path("admin/", admin.site.urls),

    # App routes
    path("api/", include("recipe.urls")),
    path("community/", include("community.urls", namespace='community')),
    path("ingredients/", include("ingredient_tracker.urls", namespace='ingredient_tracker')), 

    # Main routes
    path("", home, name="home"),
    path("ingredient-search/", IngredientSearchView.as_view(), name="ingredient_search"),
    # Remove or rename this to avoid conflict
    # path("recipe-generator/", recipe_ai, name="recipe_ai"),
    
    # Authentication routes
    path('login/', custom_login, name='login'),
    path('signup/', custom_signup, name='signup'),
    path('logout/', custom_logout, name='logout'),
    
    # Admin routes
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'), 
    path('admin-users/', admin_user, name='admin_user'),
    path('admin-panel/', include(('adminPanel.urls', 'adminPanel'), namespace='adminPanel')),

    path('notification/', include('notification.urls')),
    path('issues/', include('report_issues_user.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
