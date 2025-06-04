# ingredient_tracker/utils.py
from .models import Ingredient
from datetime import date
from notification.utils import create_expiry_notification

def get_user_ingredients(user):
    ingredients = Ingredient.objects.filter(user=user)

    for ingredient in ingredients:
        if ingredient.expiry_date:
            delta = (ingredient.expiry_date - date.today()).days
            ingredient.days_left = delta
            ingredient.status = (
                "Expired" if delta < 0
                else "Expiring Soon" if delta <= 3
                else "Fresh"
            )
            
            # Create notifications for expired or soon-to-expire ingredients
            if delta <= 3:
                create_expiry_notification(user, ingredient.id, ingredient.name, delta)
        else:
            ingredient.days_left = None
            ingredient.status = "No expiry info"
    
    def sort_key(ingredient):
        status_order = {
            "Expiring Soon": 0,
            "Fresh": 1,
            "Expired": 2,
            "No expiry info": 3,
        }
        return status_order.get(ingredient.status, 99)

    return sorted(ingredients, key=sort_key)
