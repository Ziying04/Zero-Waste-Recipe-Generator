from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

# Import any utility function you use
from recipe.utils import generate_recipe

# Import your models here
# from recipe.models import SharedResource  # Remove or comment out this line
from recipe.models import Recipe  # Import Recipe model
# from recipe.models import ForumPost  # Remove or comment out this line
# from recipe.models import Comment  # Remove or comment out this line


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


def admin_dashboard(request):
    total_users = User.objects.count()
    return render(request, 'adminPage.html', {
        'total_users': total_users,
    })

def admin_user(request):
    """Admin user management view with debugging"""
    print("=== ADMIN USER VIEW CALLED ===")
    print(f"User: {request.user}")
    
    try:
        # Get all users with detailed information
        users = User.objects.all().order_by('-date_joined')
        total_users = users.count()
        
        print(f"Found {total_users} users")
        
        # Debug: Print first few users
        for i, user in enumerate(users[:3]):
            print(f"User {i+1}: {user.username} - {user.email} - Active: {user.is_active}")
        
        # Additional filtering options (for future use)
        search_query = request.GET.get('search', '')
        if search_query:
            users = users.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
            print(f"Filtered users by '{search_query}': {users.count()} results")
        
        context = {
            'users': users,
            'total_users': total_users,
            'search_query': search_query,
        }
        
        print(f"Context: users count = {len(list(users))}, total = {total_users}")
        
    except Exception as e:
        print(f"ERROR in admin_user view: {e}")
        import traceback
        traceback.print_exc()
        
        context = {
            'users': [],
            'total_users': 0,
            'error': str(e),
        }
    
    print("=== END ADMIN USER VIEW ===")
    return render(request, "AdminUser.html", context)

def admin_content(request):
    """Admin content management view"""
    try:
        # Fetch all content types with error handling
        recipes = []
        posts = []
        comments = []
        resources = []
        
        try:
            if hasattr(Recipe, 'objects') and Recipe.objects:
                recipes = Recipe.objects.all().order_by('-created_at')
        except:
            pass
            
        try:
            if hasattr(ForumPost, 'objects') and ForumPost.objects:
                posts = ForumPost.objects.all().order_by('-created_at')
        except:
            pass
            
        try:
            if hasattr(Comment, 'objects') and Comment.objects:
                comments = Comment.objects.all().order_by('-created_at')
        except:
            pass
            
        try:
            if hasattr(SharedResource, 'objects') and SharedResource.objects:
                resources = SharedResource.objects.all().order_by('-uploaded_at')
        except:
            pass
        
        context = {
            'recipes': recipes,
            'posts': posts,
            'comments': comments,
            'resources': resources,
            'recipes_count': len(recipes),
            'posts_count': len(posts),
            'comments_count': len(comments),
            'resources_count': len(resources),
        }
        
    except Exception as e:
        print(f"ERROR in admin_content view: {e}")
        context = {
            'recipes': [],
            'posts': [],
            'comments': [],
            'resources': [],
            'error': str(e),
        }
    
    return render(request, 'admin_content.html', context)
