from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from recipe.models import Recipe
from community.models import DonationFoodPost
from django import forms
from django.views.decorators.http import require_GET
import json

def admin_dashboard(request):
    print("=== ADMIN DASHBOARD VIEW CALLED ===")
    
    try:
        total_users = User.objects.count()
        print(f"SUCCESS: Total Users = {total_users}")
        
        if total_users == 0:
            print("WARNING: No users found in database")
        else:
            users = User.objects.all()[:3]
            usernames = [user.username for user in users]
            print(f"Sample users: {usernames}")
            
    except Exception as e:
        print(f"ERROR: Could not count users - {e}")
        total_users = 0
    
    context = {
        'total_users': total_users,
    }
    
    print(f"Context being sent to template: {context}")
    print("=== END ADMIN DASHBOARD VIEW ===")
    
    return render(request, "adminPage.html", context)

def admin_user(request):
    users = User.objects.all()
    total_users = users.count()
    return render(request, "AdminUser.html", {"users": users, "total_users": total_users})

def delete_user(request, user_id):
    """
    Delete a user via AJAX request
    """
    try:
        # Get the user to delete
        user_to_delete = get_object_or_404(User, id=user_id)
        
        # Prevent deletion of superusers (additional safety check)
        if user_to_delete.is_superuser:
            return JsonResponse({
                'success': False,
                'error': 'Cannot delete superuser accounts.'
            }, status=403)  # Changed to 403 Forbidden
        
        # Prevent users from deleting themselves
        if user_to_delete.id == request.user.id:
            return JsonResponse({
                'success': False,
                'error': 'You cannot delete your own account.'
            }, status=403)  # Changed to 403 Forbidden
        
        # Store username for response
        deleted_username = user_to_delete.username
        
        # Delete the user
        user_to_delete.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'User "{deleted_username}" has been deleted successfully.',
            'deleted_user_id': user_id
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User not found.'
        }, status=404)
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error deleting user {user_id}: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=500)

def admin_content(request):
    """
    Manage content by approving, hiding, or deleting it.
    """
    recipes = Recipe.objects.select_related('user').all().order_by('-created_at')
    donation_posts = DonationFoodPost.objects.select_related('donor').all().order_by('-created_at')
    return render(request, "adminContent.html", {
        "recipes": recipes,
        "donation_posts": donation_posts,
    })

@user_passes_test(lambda u: u.is_staff)
def delete_recipe(request, recipe_id):
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, id=recipe_id)
        recipe.delete()
        return JsonResponse({"success": True})
    return HttpResponseForbidden()

@user_passes_test(lambda u: u.is_staff)
def delete_donation(request, donation_id):
    if request.method == "POST":
        post = get_object_or_404(DonationFoodPost, id=donation_id)
        post.delete()
        return JsonResponse({"success": True})
    return HttpResponseForbidden()

class RecipeEditForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'steps', 'image_url', 'ingredients', 'is_shared']

class DonationEditForm(forms.ModelForm):
    class Meta:
        model = DonationFoodPost
        fields = ['food_name', 'description', 'quantity', 'location', 'category', 'expiry_date', 'status']

@user_passes_test(lambda u: u.is_staff)
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if request.method == "POST":
        # Handle AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Get form data
                name = request.POST.get('name')
                cooking_time = request.POST.get('cooking_time')
                steps = request.POST.get('steps')
                image_url = request.POST.get('image_url')
                ingredients = request.POST.get('ingredients')
                is_shared = request.POST.get('is_shared') == 'on'
                
                # Update recipe
                recipe.name = name
                recipe.cooking_time = int(cooking_time)
                recipe.steps = steps
                recipe.image_url = image_url if image_url else ''
                recipe.ingredients = ingredients
                recipe.is_shared = is_shared
                recipe.save()
                
                return JsonResponse({
                    "success": True,
                    "message": "Recipe updated successfully",
                    "recipe": {
                        "id": recipe.id,
                        "name": recipe.name,
                        "cooking_time": recipe.cooking_time,
                        "steps": recipe.steps,
                        "image_url": recipe.image_url,
                        "ingredients": recipe.ingredients,
                        "is_shared": recipe.is_shared,
                    }
                })
            except Exception as e:
                return JsonResponse({
                    "success": False,
                    "error": str(e)
                }, status=400)
        else:
            # Handle regular form submission
            form = RecipeEditForm(request.POST, instance=recipe)
            if form.is_valid():
                form.save()
                return redirect('adminPanel:admin_content')
            else:
                return render(request, "admin_edit_recipe.html", {"form": form, "recipe": recipe})
    else:
        form = RecipeEditForm(instance=recipe)
        return render(request, "admin_edit_recipe.html", {"form": form, "recipe": recipe})

@user_passes_test(lambda u: u.is_staff)
def create_recipe(request):
    """
    Create a new recipe
    """
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Get form data
                name = request.POST.get('name')
                cooking_time = request.POST.get('cooking_time')
                steps = request.POST.get('steps')
                image_url = request.POST.get('image_url')
                ingredients = request.POST.get('ingredients')
                is_shared = request.POST.get('is_shared') == 'on'
                
                # Create new recipe
                recipe = Recipe.objects.create(
                    name=name,
                    cooking_time=int(cooking_time),
                    steps=steps,
                    image_url=image_url if image_url else '',
                    ingredients=ingredients,
                    is_shared=is_shared,
                    user=request.user  # Set the current user as the creator
                )
                
                return JsonResponse({
                    "success": True,
                    "message": "Recipe created successfully",
                    "recipe": {
                        "id": recipe.id,
                        "name": recipe.name,
                        "cooking_time": recipe.cooking_time,
                        "steps": recipe.steps,
                        "image_url": recipe.image_url,
                        "ingredients": recipe.ingredients,
                        "is_shared": recipe.is_shared,
                        "author": recipe.user.username,
                        "date": recipe.created_at.strftime('%Y-%m-%d')
                    }
                })
            except Exception as e:
                return JsonResponse({
                    "success": False,
                    "error": str(e)
                }, status=400)
    
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

@user_passes_test(lambda u: u.is_staff)
def edit_donation(request, donation_id):
    post = get_object_or_404(DonationFoodPost, id=donation_id)
    if request.method == "POST":
        form = DonationEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('adminPanel:admin_content')
    else:
        form = DonationEditForm(instance=post)
    return render(request, "admin_edit_donation.html", {"form": form, "post": post})

@require_GET
@user_passes_test(lambda u: u.is_staff)
def recipe_detail_json(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return JsonResponse({
        "id": recipe.id,
        "name": recipe.name,
        "cooking_time": recipe.cooking_time,
        "steps": recipe.steps,
        "image_url": recipe.image_url or '',
        "ingredients": recipe.ingredients,
        "is_shared": recipe.is_shared,
    })

@require_GET
@user_passes_test(lambda u: u.is_staff)
def donation_detail_json(request, donation_id):
    donation = get_object_or_404(DonationFoodPost, id=donation_id)
    return JsonResponse({
        "id": donation.id,
        "food_name": donation.food_name,
        "description": donation.description,
        "quantity": donation.quantity,
        "location": donation.location,
        "category": donation.category,
        "expiry_date": donation.expiry_date.strftime('%Y-%m-%d'),
        "status": donation.status,
    })