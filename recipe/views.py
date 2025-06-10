import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from .utils import generate_recipe, parse_ai_recipe
from .models import Recipe, UserProfile, RecipeLike
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from datetime import date
from community.models import DonationFoodPost, ClaimedFood  # Updated import
from ingredient_tracker.utils import get_user_ingredients
from ingredient_tracker.models import Ingredient  # adjust import as needed
from django.utils import timezone
from django.http import HttpResponseBadRequest


logger = logging.getLogger(__name__)
@ensure_csrf_cookie
def recipe_ai(request):

    if request.method == 'POST':
        # Check for ingredients selected via inventory checkboxes
        selected_ids = request.POST.getlist('selected_ingredients')
        print("Selected IDs:", selected_ids)
        ingredients = []

        if selected_ids:
            # Get ingredient names from DB using the selected IDs
            ingredients_queryset = Ingredient.objects.filter(id__in=selected_ids, user=request.user)
            ingredients = [ingredient.name for ingredient in ingredients_queryset]

        else:
            # Fallback to user input from textarea
            user_input = request.POST.get('user_input', '')
            ingredients = [ing.strip() for ing in user_input.split(',') if ing.strip()]

        if not ingredients:
            return HttpResponse("No ingredients selected or entered.", status=400)

        # Generate recipe using AI
        recipe_response = generate_recipe(ingredients)

        if isinstance(recipe_response, dict) and 'error' in recipe_response:
            return HttpResponse(f"Error: {recipe_response['error']}", status=500)
        
        # Parse the AI recipe and pass to template
        #parsed_recipe = parse_ai_recipe(recipe_response)
        #return render(request, "recipe_result.html", {"recipe": parsed_recipe})

        # Return recipe content
        return HttpResponse(recipe_response, content_type='text/plain')

    # GET request — show ingredient inventory
    ingredients = get_user_ingredients(request.user)
    return render(request, 'recipe_ai.html', {'ingredients': ingredients})


@csrf_exempt
def parse_recipe(request):
    if request.method == 'POST':
        raw_text = request.POST.get('raw_recipe')
        recipe = parse_ai_recipe(raw_text)

        return render(request, 'recipe_result.html', {
            'recipe': recipe
        })
    
    return HttpResponseBadRequest("Invalid method")


@csrf_exempt
def recipe_generator(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        ingredients = [x.strip() for x in user_input.split(",")]
        recipe = generate_recipe(ingredients)
        return render(request, "recipe_ai.html", {"recipe": recipe})
    
    return render(request, "recipe_ai.html")


def kitchen_view(request):
    recipes = Recipe.objects.all()
    if not request.user.is_authenticated:
        return render(request, "kitchen.html", {"recipes": recipes})
    
    # Add authentication info for the template
    liked_recipes = Recipe.objects.filter(likes=request.user).values_list('id', flat=True)
    saved_recipes = Recipe.objects.filter(saved_by=request.user).values_list('id', flat=True)
    
    return render(request, "kitchen.html", {
        "recipes": recipes,
        "liked_recipes": liked_recipes,
        "saved_recipes": saved_recipes
    })

def display_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "display.html", {"recipe": recipe})

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {"error": "Email already exists"})
        
        user = User.objects.create_user(username=email, email=email, password=password)
        profile = UserProfile.objects.create(user=user, name=name)
        login(request, user)
        messages.success(request, "Sign up successful! Please log in.")
        return redirect('recipe_ai')
    
    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect('recipe_ai')
        return render(request, "login.html", {"error": "Invalid credentials"})
    
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def collection_view(request):
    # Get recipes saved by the user (not created by the user)
    saved_recipes = Recipe.objects.filter(saved_by=request.user).select_related('user')
    return render(request, "collection.html", {"saved_recipes": saved_recipes})

@login_required
def likes_view(request):
    # Get liked recipes with all related data in one query
    liked_recipes = RecipeLike.objects.filter(user=request.user).select_related('recipe').prefetch_related('recipe__likes')
    return render(request, "like.html", {"liked_recipes": liked_recipes})

@login_required
def profile_view(request):
    return render(request, "profile.html")

@login_required
def diary_view(request):
    # Get donation counts from DonationFoodPost
    active_donations = DonationFoodPost.objects.filter(
        donor=request.user,
        status='Available'
    ).count()
    completed_donations = DonationFoodPost.objects.filter(
        donor=request.user,
        status__in=['Claimed', 'Completed']
    ).count()
    total_donations = active_donations + completed_donations

    # Get claim counts from ClaimedFood
    pending_claims = ClaimedFood.objects.filter(
        claimer=request.user,
        status='Pending'
    ).count()
    completed_claims = ClaimedFood.objects.filter(
        claimer=request.user,
        status='Completed'
    ).count()
    total_claims = pending_claims + completed_claims

    context = {
        'active_donations': active_donations,
        'completed_donations': completed_donations,
        'total_donations': total_donations,
        'pending_claims': pending_claims, 
        'completed_claims': completed_claims,
        'total_claims': total_claims,
    }
    return render(request, 'diary.html', context)

@login_required
def sharing_view(request):
    user_recipes = Recipe.objects.filter(user=request.user)
    return render(request, "sharing.html", {"user_recipes": user_recipes})

@login_required
@csrf_exempt
def toggle_save_recipe(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if recipe.saved_by.filter(id=request.user.id).exists():
            recipe.saved_by.remove(request.user)
            saved = False
            message = "Recipe removed from collection"
        else:
            recipe.saved_by.add(request.user)
            saved = True
            message = "Recipe saved to collection"
        
        return JsonResponse({
            'saved': saved,
            'count': recipe.total_saves(),
            'message': message
        })
    except Exception as e:
        logger.error(f"Error in toggle_save_recipe: {e}")
        return JsonResponse({'error': 'An error occurred while saving the recipe.'}, status=500)

@login_required
@csrf_exempt
def toggle_like_recipe(request, recipe_id):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Please login to like recipes'}, status=401)

        recipe = get_object_or_404(Recipe, id=recipe_id)
        like_exists = RecipeLike.objects.filter(user=request.user, recipe=recipe).exists()

        if like_exists:
            RecipeLike.objects.filter(user=request.user, recipe=recipe).delete()
            recipe.likes.remove(request.user)
            liked = False
            message = "Recipe removed from likes"
        else:
            RecipeLike.objects.create(user=request.user, recipe=recipe)
            recipe.likes.add(request.user)
            liked = True
            message = "Recipe added to likes"
        
        return JsonResponse({
            'liked': liked,
            'count': recipe.likes.count(),
            'message': message
        })
    except Exception as e:
        logger.error(f"Error in toggle_like_recipe: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@csrf_exempt
def update_recipe(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        
        # Check if user owns the recipe
        if recipe.user != request.user:
            return JsonResponse({'error': 'Unauthorized to edit this recipe'}, status=403)
        
        if request.method == "POST":
            data = json.loads(request.body)
            
            # Update recipe fields
            recipe.name = data.get('name', recipe.name)
            recipe.cooking_time = int(data.get('cooking_time', recipe.cooking_time))
            recipe.ingredients = data.get('ingredients', recipe.ingredients)
            recipe.steps = data.get('steps', recipe.steps)
            
            recipe.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Recipe updated successfully'
            })
            
    except Exception as e:
        logger.error(f"Error updating recipe: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def edit_recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if user owns the recipe
    if recipe.user != request.user:
        return redirect('sharing')
        
    return render(request, "edit_recipe.html", {"recipe": recipe})

@login_required
@csrf_exempt
def toggle_share_recipe(request, recipe_id):
    """Toggle the shared status of a recipe"""
    try:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        
        # Only the recipe owner can share/unshare it
        if recipe.user != request.user:
            return JsonResponse({'error': 'You cannot share/unshare this recipe'}, status=403)
            
        # Toggle the shared status
        recipe.is_shared = not recipe.is_shared
        
        # If sharing, record the timestamp
        if recipe.is_shared:
            recipe.shared_at = timezone.now()
            message = "Recipe shared successfully! It's now visible to the community."
        else:
            message = "Recipe is now private and only visible to you."
            
        recipe.save()
        
        return JsonResponse({
            'is_shared': recipe.is_shared,
            'message': message
        })
    except Exception as e:
        logger.error(f"Error in toggle_share_recipe: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)
    

@login_required
def share_recipe(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            cooking_time = request.POST.get('cooking_time')

            ingredients = request.POST.get('ingredients')
            if isinstance(ingredients, list):
                 ingredients = "<br>".join(ingredients)
            elif isinstance(ingredients, str):
                 ingredients = "<br>".join(ingredients.splitlines())

            steps = request.POST.get('steps')
            if isinstance(steps, list):
                 ingredients = "<br>".join(ingredients)
            elif isinstance(steps, str):
                 ingredients = "<br>".join(ingredients.splitlines())

            image_url = request.POST.get('image_url')

            # If ingredients is a list, join it into a string
            if isinstance(ingredients, list):
                ingredients = " ".join(ingredients)
            
            # Validate required fields
            if not name or not cooking_time or not ingredients or not steps:
                messages.error(request, "Missing required recipe data.")
                return redirect('recipe_ai')

            
            # Create the recipe
            recipe = Recipe.objects.create(
                name=name,
                cooking_time=int(cooking_time),
                ingredients=ingredients,
                steps=steps,
                image_url=image_url if image_url else None,
                user=request.user
            )
            
            # Automatically save to the user's collection
            recipe.saved_by.add(request.user)
            
            messages.success(request, f'Recipe "{name}" created successfully!')
            return redirect('collection')
            
        except Exception as e:
            logger.error(f"Error creating recipe: {e}")
            messages.error(request, f"An error occurred while saving the recipe.")
            return redirect('recipe_ai')
    
    # GET request - show the recipe post display
    return redirect('recipe_ai')

@login_required
def create_recipe_view(request):
    """View for creating a new recipe"""
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            cooking_time = request.POST.get('cooking_time')
            ingredients = request.POST.get('ingredients')
            steps = request.POST.get('steps')
            image_url = request.POST.get('image_url')
            
            # Validate required fields
            if not name or not cooking_time or not ingredients or not steps:
                return render(request, 'create_recipe.html', {
                    'error': 'Please fill in all required fields.'
                })
            
            # Create the recipe
            recipe = Recipe.objects.create(
                name=name,
                cooking_time=int(cooking_time),
                ingredients=ingredients,
                steps=steps,
                image_url=image_url if image_url else None,
                user=request.user
            )
            
            # Automatically save to the user's collection
            recipe.saved_by.add(request.user)
            
            messages.success(request, f'Recipe "{name}" created successfully!')
            return redirect('collection')
            
        except Exception as e:
            logger.error(f"Error creating recipe: {e}")
            return render(request, 'create_recipe.html', {
                'error': f'An error occurred: {str(e)}'
            })
    
    # GET request - show the form
    return render(request, 'create_recipe.html')

