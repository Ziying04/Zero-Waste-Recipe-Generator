from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

# Import any utility function you use
from recipe.utils import generate_recipe


# Home view (redirects to recipe_ai if authenticated)
def home(request):
    if request.user.is_authenticated:
        return redirect('recipe_ai')  # must match the name in urls.py

    if request.method == "POST":
        if "find_recipes" in request.POST:
            return redirect('ingredient_search')  # update with your recipe page url name
        elif "use_ai_recipe" in request.POST:
            return redirect('recipe_ai')  # update with your AI recipe generator url name

    return render(request, 'home.html')


# View to render the AI recipe page
def recipe_ai(request):
    return render(request, "recipe_ai.html")


# Ingredient Search View
@method_decorator(ensure_csrf_cookie, name='dispatch')
class IngredientSearchView(View):
    def get(self, request):
        ingredients = request.session.get("ingredients", [])
        return render(request, ".html", {"ingredients": ingredients})

    def post(self, request):
        ingredients = request.session.get("ingredients", [])

        if "add" in request.POST:
            ingredient = request.POST.get("ingredient", "").strip()
            if ingredient and ingredient not in ingredients:
                ingredients.append(ingredient)

        elif "remove" in request.POST:
            to_remove = request.POST.get("remove")
            if to_remove in ingredients:
                ingredients.remove(to_remove)

        elif "find" in request.POST:
            # You could run generate_recipe(ingredients) here
            pass  # Placeholder

        request.session["ingredients"] = ingredients
        return redirect("ingredient_search")


def custom_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check for admin credentials
        if email == "admin123@gmail.com" and password == "admin123":
            # Try to get or create the admin user
            user, created = User.objects.get_or_create(username="admin123", defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            })
            if created:
                user.set_password(password)
                user.save()
            # Authenticate and login
            user = authenticate(request, username="admin123", password=password)
            if user:
                login(request, user)
                return redirect("admin_dashboard")  # url name for adminPage.html
        # Normal authentication for other users
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")
