from django.contrib import admin
from .models import Ingredient

# Register your models here.

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'expiry_date', 'user')