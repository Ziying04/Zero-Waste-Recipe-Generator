from django.shortcuts import render
from .models import Ingredient
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .utils import get_user_ingredients 


# Create your views here.
@login_required
def expiring_tracker_view(request):
    ingredients = get_user_ingredients(request.user)

    if ingredients:
        return redirect('ingredient_tracker:get_ingredients')

    return render(request, 'expiring_tracker.html')

@login_required
@csrf_exempt
def add_ingredient(request):
    if request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        category = request.POST.get("category")
        location = request.POST.get("location")
        purchase_date = request.POST.get("purchaseDate")
        expiry_date = request.POST.get("expiryDate")
        notes = request.POST.get("notes")
        
        # Save to DB (basic version)
        Ingredient.objects.create(
            user=request.user, 
            name=name,
            quantity=quantity,
            category=category,
            location=location,
            purchase_date=purchase_date,
            expiry_date=expiry_date,
            notes=notes
        )
        messages.success(request, "Ingredient added successfully!") 
        return redirect('ingredient_tracker:get_ingredients')  # Redirect after successful POST

    return render(request, 'expiring_tracker.html')

@login_required
def delete_ingredient(request, ingredient_id):
     ingredient = get_object_or_404(Ingredient, id=ingredient_id, user=request.user)
     ingredient.delete()
     return redirect('ingredient_tracker:get_ingredients')

@login_required
def get_ingredients(request):
    ingredients = get_user_ingredients(request.user)
    any_expiring_soon = any(i.status == "Expiring Soon" for i in ingredients)

    return render(request, 'expiring_tracker.html', {
        'ingredients': ingredients,
        'any_expiring_soon': any_expiring_soon
    })

