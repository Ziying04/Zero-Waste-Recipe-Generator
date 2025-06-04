from .models import Notification
from django.urls import reverse

def create_like_notification(user, recipe_id, liker_username):
    """
    Create a notification when someone likes a user's recipe
    """
    content = f"{liker_username} liked your recipe"
    link = reverse('recipe_detail', args=[recipe_id])  # Adjust this URL name to your actual recipe detail view
    
    Notification.objects.create(
        user=user,
        notification_type='like',
        content=content,
        link=link,
        related_id=recipe_id
    )

def create_expiry_notification(user, ingredient_id, ingredient_name, days_left):
    """
    Create a notification for expiring ingredients
    """
    if days_left <= 0:
        content = f"Your ingredient '{ingredient_name}' has expired!"
    else:
        content = f"Your ingredient '{ingredient_name}' will expire in {days_left} days"
    
    link = reverse('ingredient_tracker:get_ingredients')
    
    # Check if a notification for this ingredient already exists and is unread
    existing = Notification.objects.filter(
        user=user,
        notification_type='expiry',
        related_id=ingredient_id,
        is_read=False
    ).exists()
    
    # Only create a new notification if one doesn't already exist for this ingredient
    if not existing:
        Notification.objects.create(
            user=user,
            notification_type='expiry',
            content=content,
            link=link,
            related_id=ingredient_id
        )

def create_admin_warning(user, warning_message):
    """
    Create an admin warning notification
    """
    Notification.objects.create(
        user=user,
        notification_type='admin_warning',
        content=warning_message
    )
