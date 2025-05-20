from django.contrib import admin
from .models import DonationFoodPost, ClaimedFood

# Register models
admin.site.register(DonationFoodPost)
admin.site.register(ClaimedFood)
