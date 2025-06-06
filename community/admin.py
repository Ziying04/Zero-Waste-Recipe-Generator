from django.contrib import admin
from .models import DonationFoodPost, ClaimedFood

@admin.register(DonationFoodPost)
class DonationFoodPostAdmin(admin.ModelAdmin):
    list_display = ['food_name', 'donor', 'category', 'status', 'expiry_date', 'created_at']
    list_filter = ['status', 'category', 'created_at', 'expiry_date']
    search_fields = ['food_name', 'donor__username', 'location']
    readonly_fields = ['created_at']
    list_editable = ['status']

@admin.register(ClaimedFood)
class ClaimedFoodAdmin(admin.ModelAdmin):
    list_display = ['food_post', 'claimer', 'status', 'claimed_date']
    list_filter = ['status', 'claimed_date']
    search_fields = ['food_post__food_name', 'claimer__username']
    readonly_fields = ['claimed_date']
    list_editable = ['status']
