from django.contrib import admin
from .models import Recipe, RecipeLike  # Import RecipeLike

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time', 'image_url', 'ingredients')  # Include ingredients in admin display

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeLike)  # Register the new model
