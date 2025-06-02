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

# Import directly from ai_recipe.views
from ai_recipe.views import IngredientSearchView, recipe_ai
from ai_recipe.views import home, custom_login
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),

    # App routes
    path("api/", include("recipe.urls")),
    path("community/", include("community.urls", namespace='community')),
    path("ingredients/", include("ingredient_tracker.urls", namespace='ingredient_tracker')), 

    # Main routes
    path("", home, name="home"),
    path("ingredient-search/", IngredientSearchView.as_view(), name="ingredient_search"),
    path("recipe-generator/", recipe_ai, name="recipe_generator"),

    # Login and admin dashboard
    path('login/', custom_login, name='login'),
    path('admin-dashboard/', TemplateView.as_view(template_name="adminPage.html"), name='admin_dashboard'),
    path('admin-users/', TemplateView.as_view(template_name="AdminUser.html"), name='admin_user'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
