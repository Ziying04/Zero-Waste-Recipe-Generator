from django.urls import path
from .views import (
    community_view, 
    share_food, 
    SeekerDashboardView, 
    DonorDashboardView,
    donation_food_view,
    claimed_food_view,
    donors_view,
    claim_donation,
    mark_received,
    delete_donation,
)

app_name = 'community'

urlpatterns = [
    path('', community_view, name='community'),
    path('share/', share_food, name='share_food'),
    path('donors/', donors_view, name='donors'),
    path('seekers/', SeekerDashboardView.as_view(), name='seekers'),
    path('donation_food/', donation_food_view, name='donation_food'),
    path('claimed_food/', claimed_food_view, name='claimed_food'),
    path('claim_donation/<int:post_id>/', claim_donation, name='claim_donation'),
    path('mark_received/<int:claim_id>/', mark_received, name='mark_received'),
    path('delete_donation/<int:post_id>/', delete_donation, name='delete_donation'),
]
