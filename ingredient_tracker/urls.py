from django.urls import path
from .views import (
    expiring_tracker_view,
    get_ingredients,
    add_ingredient,
    delete_ingredient,
)

app_name = 'ingredient_tracker'

urlpatterns = [
    path("", expiring_tracker_view, name='expiring_tracker'),
    path("add_ingredient/", add_ingredient, name='add_ingredient'),
    path("delete_ingredient/<int:ingredient_id>/", delete_ingredient, name='delete_ingredient'),
    path("get_ingredients/", get_ingredients, name='get_ingredients'),
]