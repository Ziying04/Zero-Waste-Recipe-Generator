from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import DonationFoodPost, ClaimedFood
from django.views.decorators.http import require_POST
import json
from django.contrib import messages
from django.utils import timezone

# Replace with actual user's coordinates or extract from request/user profile
DEFAULT_USER_LOCATION = (3.1390, 101.6869)  # Example: Kuala Lumpur lat/lon

def community_view(request):
    """Community landing page with real statistics"""
    try:
        # Get real statistics from database
        total_users = User.objects.filter(is_active=True).count()
        
        # Total food donations ever posted
        total_donations = DonationFoodPost.objects.count()
        
        # Completed food transfers (claimed and completed)
        completed_transfers = ClaimedFood.objects.filter(
            status__in=['Completed', 'Received']
        ).count()
        
        # Alternative: Count donations that have been claimed
        # completed_transfers = DonationFoodPost.objects.filter(
        #     status__in=['Claimed', 'Completed']
        # ).count()
        
        # Active food posts currently available
        active_donations = DonationFoodPost.objects.filter(
            status='Available'
        ).count()
        
        context = {
            'total_users': total_users,
            'total_donations': total_donations,
            'completed_transfers': completed_transfers,
            'active_donations': active_donations,
        }
        
    except Exception as e:
        # Fallback values in case of database error
        context = {
            'total_users': 0,
            'total_donations': 0,
            'completed_transfers': 0,
            'active_donations': 0,
        }
    
    return render(request, 'community.html', context)

def share_food(request):
    return render(request, 'donors.html')

@login_required
def donation_food_view(request):
    # Get the user's donations
    donations = DonationFoodPost.objects.filter(donor=request.user)
    context = {
        'donations': donations,
        'active_donations': donations.filter(status='Available').count(),
        'completed_donations': donations.filter(status='Completed').count(),
    }
    return render(request, 'donors.html', context)

@login_required
def claimed_food_view(request):
    # Get the foods claimed by the user
    claimed_food = ClaimedFood.objects.filter(claimer=request.user).select_related('food_post')
    context = {
        'claimed_food': claimed_food,
        'pending_claims': claimed_food.filter(status='Pending').count(),
        'completed_claims': claimed_food.filter(status='Completed').count(),
    }
    return render(request, 'claimed_food.html', context)

class SeekerDashboardView(TemplateView):
    template_name = 'seekers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('search', '')
        category_filter = self.request.GET.get('category', '')
        max_distance = float(self.request.GET.get('distance', 10))

        # Get all available donations 
        food_posts = DonationFoodPost.objects.filter(status='Available').order_by('-created_at')

        if search_term:
            food_posts = food_posts.filter(
                Q(food_name__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(category__icontains=search_term)
            )

        if category_filter:
            food_posts = food_posts.filter(category=category_filter)

        # Get claimed food for the current user
        claimed_food = []
        if self.request.user.is_authenticated:
            claimed_food = ClaimedFood.objects.filter(
                claimer=self.request.user
            ).select_related('food_post', 'food_post__donor').order_by('-claimed_date')

        context.update({
            'donations': food_posts,
            'claimed_food': claimed_food,
            'search_term': search_term,
            'category_filter': category_filter,
            'max_distance': max_distance,
            'categories': [
                'Fruits', 'Vegetables', 'Dairy', 'Grains & Bread',
                'Protein', 'Prepared Meals', 'Canned Goods', 'Other'
            ],
            'user_lat': self.request.GET.get('user_lat', ''),
            'user_lon': self.request.GET.get('user_lon', '')
        })
        return context

class DonorDashboardView(TemplateView):
    template_name = 'donors.html'

@login_required
def donors_view(request):
    if request.method == 'POST':
        food_name = request.POST.get('title')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        location = request.POST.get('location')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        expiry_date = request.POST.get('expiration_date')

        DonationFoodPost.objects.create(
            donor=request.user,
            food_name=food_name,
            description=description,
            quantity=quantity,
            location=location,
            category=category,
            image=image,
            expiry_date=expiry_date
        )
        return redirect('community:donors')

    # Only get the user's own donation posts
    donation_posts = DonationFoodPost.objects.filter(donor=request.user).order_by('-created_at')
    return render(request, 'donors.html', {'DonationFoodPost': donation_posts})

@login_required
def claim_donation(request, post_id):
    post = get_object_or_404(DonationFoodPost, id=post_id)
    
    # Check if post is available
    if post.status != 'Available':
        messages.error(request, f"Sorry, this donation is no longer available.")
        return redirect('community:seekers')
    
    # Mark the post as claimed
    post.status = 'Claimed'
    post.save()
    
    # Create a claim record
    claim = ClaimedFood.objects.create(
        food_post=post,
        claimer=request.user,
        claimed_date=timezone.now(),
        status='Pending'
    )
    
    messages.success(request, f"You have successfully claimed '{post.food_name}'")
    return redirect('community:seekers')

@login_required
def mark_received(request, claim_id):
    claim = get_object_or_404(ClaimedFood, id=claim_id, claimer=request.user)
    
    # Update claim status
    claim.status = 'Completed'
    claim.save()
    
    # Update food post status if needed
    food_post = claim.food_post
    food_post.status = 'Completed'
    food_post.save()
    
    messages.success(request, f"Marked '{food_post.food_name}' as received. Thank you!")
    return redirect('community:seekers')

@login_required
def delete_donation(request, post_id):
    """
    Delete a donation food post and any associated claims.
    Only the owner (donor) of the post can delete it.
    """
    post = get_object_or_404(DonationFoodPost, id=post_id)
    
    # Check if the current user is the owner of the post
    if post.donor != request.user:
        messages.error(request, "You don't have permission to delete this donation.")
        return redirect('community:donors')
    
    # Delete any claims associated with this post
    ClaimedFood.objects.filter(food_post=post).delete()
    
    # Delete the post itself
    post_name = post.food_name
    post.delete()
    
    # Return JSON response for AJAX requests or redirect for regular requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f'"{post_name}" has been deleted successfully.'
        })
    
    messages.success(request, f'"{post_name}" has been deleted successfully.')
    return redirect('community:donors')



