from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from recipe.models import Recipe
from django.views.decorators.http import require_POST
from report_issues_user.models import IssueReport
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from recipe.models import Recipe
from community.models import DonationFoodPost
from django import forms
from django.views.decorators.http import require_GET
import json
# Removed ForumPost from the import list

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

    try:
        # Try to use the same model as the main admin dashboard
        from report_issues_user.models import IssueReport
        total_issues = IssueReport.objects.count()
        open_issues = IssueReport.objects.filter(status='open').count()
        resolved_issues = IssueReport.objects.filter(status='resolved').count()
        print(f"SUCCESS: Using report_issues_user.models - Total Issues = {total_issues} (Open: {open_issues}, Resolved: {resolved_issues})")
        
    except ImportError:
        try:
            # Fallback to local adminPanel model
            from .models import IssueReport
            total_issues = IssueReport.objects.count()
            open_issues = IssueReport.objects.filter(status='open').count()
            resolved_issues = IssueReport.objects.filter(status='resolved').count()
            print(f"SUCCESS: Using adminPanel.models - Total Issues = {total_issues} (Open: {open_issues}, Resolved: {resolved_issues})")
            
        except Exception as e:
            print(f"ERROR: Could not count issues with adminPanel.models - {e}")
            total_issues = 0
            open_issues = 0
            resolved_issues = 0
            
    except Exception as e:
        print(f"ERROR: Could not count issues - {e}")
        total_issues = 0
        open_issues = 0
        resolved_issues = 0

    context = {
        'total_users': total_users,
        'total_issues': total_issues,
        'open_issues': open_issues,
        'resolved_issues': resolved_issues,
    }
    print(f"Context being sent to template: {context}")
    print("=== END ADMIN DASHBOARD VIEW ===")
    
    return render(request, "adminPage.html", context)
    
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
            }, status=403)
        
        # Prevent users from deleting themselves
        if user_to_delete.id == request.user.id:
            return JsonResponse({
                'success': False,
                'error': 'You cannot delete your own account.'
            }, status=403)
        
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

def admin_issues(request):
    """
    Display all issues for admin management - with debugging
    """
    # Check if user is authenticated and is_staff
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "You have been logged out from admin mode.")
        return redirect('login')  # or your login page

    try:
        # Try to use the main IssueReport model first
        from report_issues_user.models import IssueReport
        print("SUCCESS: Using report_issues_user.models.IssueReport")
        
    except ImportError:
        try:
            # Fallback to adminPanel model
            from .models import IssueReport
            print("SUCCESS: Using adminPanel.models.IssueReport")
            
        except ImportError:
            print("ERROR: Could not import any IssueReport model")
            # Return empty context
            context = {
                'issues': [],
                'total_issues': 0,
                'resolved_issues': 0,
                'open_issues': 0,
                'error': 'Could not import IssueReport model'
            }
            return render(request, 'adminIssues.html', context)
    
    issues = IssueReport.objects.all().order_by('-created_at')
    total_issues = issues.count()
    resolved_issues = issues.filter(status='resolved').count()
    open_issues = total_issues - resolved_issues
    
    print(f"Found {total_issues} issues total ({open_issues} open, {resolved_issues} resolved)")

    # Debug: Print field information for the first issue
    if issues.exists():
        first_issue = issues.first()
        print("=== DEBUG: IssueReport Model Fields ===")
        
        # Print all field names
        field_names = [field.name for field in first_issue._meta.fields]
        print(f"All fields: {field_names}")
        print("=== END DEBUG ===")

    context = {
        'issues': issues,
        'total_issues': total_issues,
        'resolved_issues': resolved_issues,
        'open_issues': open_issues,
    }

    return render(request, 'adminIssues.html', context)

def issue_detail(request, issue_id):
    """
    Display detailed view of a specific issue
    """
    issue = get_object_or_404(IssueReport, pk=issue_id)
    
    context = {
        'issue': issue,
    }
    
    return render(request, 'adminIssueDetail.html', context)

def resolve_issue(request, issue_id):
    """
    Mark an issue as resolved
    """
    if request.method == "POST":
        issue = get_object_or_404(IssueReport, pk=issue_id)
        issue.status = 'resolved'
        issue.save()
        messages.success(request, "Issue marked as resolved.")
    return redirect('adminPanel:admin_issues')

def delete_issue(request, issue_id):
    """
    Delete an issue
    """
    if request.method == "POST":
        issue = get_object_or_404(IssueReport, pk=issue_id)
        issue.delete()
        messages.success(request, "Issue deleted.")
    return redirect('adminPanel:admin_issues')

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
                
                # Update the EXISTING recipe (not create new)
                recipe.name = name
                recipe.cooking_time = int(cooking_time) if cooking_time else 0
                recipe.steps = steps
                recipe.image_url = image_url if image_url else ''
                recipe.ingredients = ingredients
                recipe.is_shared = is_shared
                recipe.save()  # This updates the existing recipe
                
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
                        "author": recipe.user.username,
                        "date": recipe.created_at.strftime('%Y-%m-%d')
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

# Add this function to your views.py file

@user_passes_test(lambda u: u.is_staff)
def create_donation(request):
    """
    Create a new donation post
    """
    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Get form data
                food_name = request.POST.get('food_name')
                description = request.POST.get('description')
                quantity = request.POST.get('quantity')
                location = request.POST.get('location')
                category = request.POST.get('category')
                expiry_date = request.POST.get('expiry_date')
                status = request.POST.get('status', 'available')
                
                # Create new donation post
                donation = DonationFoodPost.objects.create(
                    food_name=food_name,
                    description=description,
                    quantity=quantity,
                    location=location,
                    category=category,
                    expiry_date=expiry_date if expiry_date else None,
                    status=status,
                    donor=request.user  # Set the current user as the donor
                )
                
                return JsonResponse({
                    "success": True,
                    "message": "Donation post created successfully",
                    "donation": {
                        "id": donation.id,
                        "food_name": donation.food_name,
                        "description": donation.description,
                        "quantity": donation.quantity,
                        "location": donation.location,
                        "category": donation.category,
                        "expiry_date": donation.expiry_date.strftime('%Y-%m-%d') if donation.expiry_date else None,
                        "status": donation.status,
                        "author": donation.donor.username,
                        "created_at": donation.created_at.strftime('%Y-%m-%d') if hasattr(donation, 'created_at') else ''
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
        # Handle AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                print(f"=== EDITING DONATION {donation_id} ===")
                print(f"POST data: {request.POST}")
                
                # Extract fields from the form data with better validation
                food_name = request.POST.get('food_name', '').strip()
                description = request.POST.get('description', '').strip()
                quantity = request.POST.get('quantity', '').strip()
                location = request.POST.get('location', '').strip()
                category = request.POST.get('category', '').strip()
                expiry_date_str = request.POST.get('expiry_date', '').strip()
                status = request.POST.get('status', 'available').strip()
                
                # Validate required fields
                if not food_name:
                    return JsonResponse({'success': False, 'error': 'Food name is required'}, status=400)
                if not description:
                    return JsonResponse({'success': False, 'error': 'Description is required'}, status=400)
                if not quantity:
                    return JsonResponse({'success': False, 'error': 'Quantity is required'}, status=400)
                if not location:
                    return JsonResponse({'success': False, 'error': 'Location is required'}, status=400)
                
                # Update fields
                post.food_name = food_name
                post.description = description
                post.quantity = quantity
                post.location = location
                post.category = category
                post.status = status
                
                # Handle expiry date
                if expiry_date_str:
                    try:
                        from datetime import datetime
                        post.expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                    except ValueError as date_error:
                        print(f"Date parsing error: {date_error}")
                        return JsonResponse({'success': False, 'error': 'Invalid date format'}, status=400)
                else:
                    post.expiry_date = None
                
                # Save the post
                post.save()
                print(f"SUCCESS: Donation {donation_id} updated successfully")
                
                # Get the correct author field - check which field exists
                author_name = ''
                if hasattr(post, 'donor') and post.donor:
                    author_name = post.donor.username
                elif hasattr(post, 'user') and post.user:
                    author_name = post.user.username
                else:
                    author_name = 'Unknown'
                
                return JsonResponse({
                    "success": True,
                    "message": "Donation post updated successfully",
                    "donation": {
                        "id": post.id,
                        "food_name": post.food_name,
                        "description": post.description,
                        "quantity": post.quantity,
                        "location": post.location,
                        "category": post.category,
                        "expiry_date": post.expiry_date.strftime('%Y-%m-%d') if post.expiry_date else '',
                        "status": post.status,
                        "author": author_name,
                        "updated_at": post.updated_at.strftime('%Y-%m-%d') if hasattr(post, 'updated_at') else '',
                        "created_at": post.created_at.strftime('%Y-%m-%d') if hasattr(post, 'created_at') else ''
                    }
                })
                
            except Exception as e:
                print(f"ERROR in edit_donation: {str(e)}")
                import traceback
                traceback.print_exc()
                return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'}, status=500)

        # Fallback to regular form submission
        else:
            form = DonationEditForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('adminPanel:admin_content')
            else:
                print(f"Form errors: {form.errors}")
                return render(request, "admin_edit_donation.html", {"form": form, "post": post})

    else:
        form = DonationEditForm(instance=post)

    return render(request, "admin_edit_donation.html", {"form": form, "post": post})

# Add this temporary debug function to your views.py
@user_passes_test(lambda u: u.is_staff)
def debug_donation_model(request, donation_id):
    """Temporary debug function to check model structure"""
    try:
        post = get_object_or_404(DonationFoodPost, id=donation_id)
        
        # Get all field names
        field_names = [field.name for field in post._meta.fields]
        
        # Get field values
        field_values = {}
        for field_name in field_names:
            try:
                field_values[field_name] = getattr(post, field_name)
            except:
                field_values[field_name] = "ERROR_GETTING_VALUE"
        
        debug_info = {
            "model_name": post.__class__.__name__,
            "field_names": field_names,
            "field_values": field_values,
            "has_donor": hasattr(post, 'donor'),
            "has_user": hasattr(post, 'user'),
        }
        
        return JsonResponse(debug_info, indent=2)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Add this URL to your urls.py temporarily:
# path('debug/donation/<int:donation_id>/', debug_donation_model, name='debug_donation'),

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
    """Return donation details as JSON for modal population"""
    post = get_object_or_404(DonationFoodPost, id=donation_id)
    
    data = {
        "success": True,
        "id": post.id,
        "food_name": post.food_name,
        "description": post.description,
        "quantity": post.quantity,
        "location": post.location,
        "category": post.category,
        "expiry_date": post.expiry_date.strftime('%Y-%m-%d') if post.expiry_date else '',
        "status": post.status,
        "author": post.donor.username if hasattr(post, 'donor') else '',
        "created_at": post.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(post, 'created_at') else '',
    }

    return JsonResponse(data)

@user_passes_test(lambda u: u.is_staff)
def create_user(request):
    """
    Create a new user with specified role
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)
    
    # Check if request is AJAX
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
    
    try:
        # Parse JSON data from request
        data = json.loads(request.body)
        
        # Extract user data
        email = data.get('email', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        role = data.get('role', 'user')
        
        # Validate required fields
        if not email or not username or not password:
            return JsonResponse({"success": False, "error": "Email, username and password are required"}, status=400)
            
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": "Username already exists"}, status=400)
            
        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "error": "Email already exists"}, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Set role based on selection
        if role == 'staff':
            user.is_staff = True
            user.save()
        elif role == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()
        
        return JsonResponse({
            "success": True,
            "message": f"User '{username}' created successfully with {role} role",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "date_joined": user.date_joined.strftime('%Y-%m-%d')
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@user_passes_test(lambda u: u.is_staff)
def add_user_view(request):
    """Render the add user form page"""
    return render(request, 'AddUser.html')