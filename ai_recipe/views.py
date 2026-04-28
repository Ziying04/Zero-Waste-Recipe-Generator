from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from adminPanel.models import IssueReport  # Import the admin panel IssueReport model

# Import any utility function you use
from recipe.utils import generate_recipe

# Import your models here
# from recipe.models import SharedResource  # Remove or comment out this line
from recipe.models import Recipe  # Import Recipe model
# from recipe.models import ForumPost  # Remove or comment out this line
# from recipe.models import Comment  # Remove or comment out this line
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def custom_login(request):
    # Redirect authenticated users
    if request.user.is_authenticated:
        return redirect('home')
        
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
                return redirect("admin_dashboard")
                
        # Normal authentication for other users
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")

def custom_signup(request):
    # Redirect authenticated users
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Enhanced validation
        errors = []
        
        # Validate name
        if not name or len(name.strip()) < 2:
            errors.append("Name must be at least 2 characters long")
            
        # Validate email
        if not email:
            errors.append("Email is required")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("Please enter a valid email address")

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            errors.append("User with this email already exists")

        # Enhanced password validation
        if not password:
            errors.append("Password is required")
        else:
            # Check password strength
            password_errors = validate_password_strength(password, email, name)
            errors.extend(password_errors)
            
            # Django's built-in password validation
            try:
                validate_password(password)
            except ValidationError as e:
                errors.extend(e.messages)

        wants_json = request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json'

        if errors:
            error_message = "; ".join(errors)
            if wants_json:
                return JsonResponse({"error": error_message}, status=400)
            return render(request, "signup.html", {"error": error_message})
        
        try:
            # Create new user
            print("TRYING TO CREATE USER...")
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=password,
                first_name=name.strip()
            )

            print("USER CREATED:", user)
            
            # Authenticate and login
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                if wants_json:
                    return JsonResponse({"success": True, "redirect": "/"})
                return redirect("home")
                
        except Exception as e:
            print("Signup error:", e)
            if wants_json:
                return JsonResponse({"error": "Failed to create account"}, status=400)
            return render(request, "signup.html", {"error": "Failed to create account"})
    
    return render(request, "signup.html")

def validate_password_strength(password, email=None, name=None):
    """Custom password strength validation"""
    errors = []
    
    # Length check
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    # Character type checks
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    # Common password check
    common_passwords = [
        'password', '123456', 'password123', 'admin', 'qwerty', 
        'letmein', '123456789', 'welcome', 'monkey', 'dragon'
    ]
    if password.lower() in common_passwords:
        errors.append("This password is too common. Please choose a stronger password")
    
    # Personal information check
    if email and email.split('@')[0].lower() in password.lower():
        errors.append("Password should not contain your email address")
    
    if name and name.lower() in password.lower():
        errors.append("Password should not contain your name")
    
    # Sequential characters check
    if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)', password.lower()):
        errors.append("Password should not contain sequential characters")
    
    # Repeated characters check
    if re.search(r'(.)\1{2,}', password):
        errors.append("Password should not contain repeated characters")
    
    return errors


# Home view (redirects to recipe_ai if authenticated)
def home(request):
    if request.method == "POST":
        # Require authentication for POST actions
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to access this feature.")
            return redirect('login')
            
        if "find_recipes" in request.POST:
            return redirect('ingredient_search')  # update with your recipe page url name
        elif "use_ai_recipe" in request.POST:
            return redirect('recipe_ai')  # update with your AI recipe generator url name

    return render(request, 'home.html')


# View to render the AI recipe page
@login_required
def recipe_ai(request):
    return render(request, "recipe_ai.html")

# Ingredient Search View
@method_decorator(ensure_csrf_cookie, name='dispatch')
@method_decorator(login_required, name='dispatch')
class IngredientSearchView(View):
    def get(self, request):
        ingredients = request.session.get("ingredients", [])
        return render(request, "ingredient_search.html", {"ingredients": ingredients})

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


def custom_logout(request):
    """Custom logout view with admin mode detection"""
    was_admin = request.user.is_staff or request.user.is_superuser if request.user.is_authenticated else False
    logout(request)
    
    if was_admin:
        messages.success(request, "You have been logged out from admin mode.")
    else:
        messages.success(request, "You have been logged out successfully.")
    
    return redirect('home')

@login_required
def admin_dashboard(request):
    """Enhanced admin dashboard with user mode toggle capability"""
    # Check if user has admin privileges
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('home')
    
    try:
        total_users = User.objects.count()
        print(f"SUCCESS: Total Users = {total_users}")
    except Exception as e:
        print(f"ERROR: Could not count users - {e}")
        total_users = 0

    try:
        # Try to import from report_issues_user app first (this seems to be the main one)
        from report_issues_user.models import IssueReport as UserIssueReport
        total_issues = UserIssueReport.objects.count()
        open_issues = UserIssueReport.objects.filter(status='open').count()
        resolved_issues = UserIssueReport.objects.filter(status='resolved').count()
        print(f"SUCCESS: Using report_issues_user.models - Total Issues = {total_issues} (Open: {open_issues}, Resolved: {resolved_issues})")
        
    except ImportError:
        try:
            # Fallback to adminPanel.models
            from adminPanel.models import IssueReport as AdminIssueReport
            total_issues = AdminIssueReport.objects.count()
            open_issues = AdminIssueReport.objects.filter(status='open').count()
            resolved_issues = AdminIssueReport.objects.filter(status='resolved').count()
            print(f"SUCCESS: Using adminPanel.models - Total Issues = {total_issues} (Open: {open_issues}, Resolved: {resolved_issues})")
            
        except ImportError:
            print("ERROR: Could not import any IssueReport model")
            total_issues = 0
            open_issues = 0
            resolved_issues = 0
            
    except Exception as e:
        print(f"ERROR: Could not count issues - {e}")
        total_issues = 0
        open_issues = 0
        resolved_issues = 0
    
    # Add admin mode context
    context = {
        'total_users': total_users,
        'total_issues': total_issues,
        'open_issues': open_issues,
        'resolved_issues': resolved_issues,
        'is_admin_mode': True,
        'admin_user': request.user,
        'can_switch_mode': True,
    }
    
    print(f"Context being sent to template: {context}")
    
    return render(request, 'adminPage.html', context)

@login_required
def admin_user(request):
    """Admin user management view with debugging"""
    # Check if user has admin privileges
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('home')
    
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

@login_required
def admin_content(request):
    """Admin content management view"""
    # Check if user has admin privileges
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('home')
    
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

@login_required
def report_issue(request):
    if request.method == 'POST':
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')
        screenshot = request.FILES.get('screenshot')
        user = request.user

        IssueReport.objects.create(
            user=user,
            issue_type=issue_type,
            description=description,
            screenshot=screenshot
        )
        return render(request, 'reportIssues_user.html', {'success': True})
    return render(request, 'reportIssues_user.html')  # GET request handling
