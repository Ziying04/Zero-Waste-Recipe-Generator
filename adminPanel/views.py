from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Recipe, Donation, ForumPost, Comment, SharedResource

def admin_dashboard(request):
    print("=== ADMIN DASHBOARD VIEW CALLED ===")  # This should always appear
    
    try:
        total_users = User.objects.count()
        print(f"SUCCESS: Total Users = {total_users}")
        
        # Check if we have any users
        if total_users == 0:
            print("WARNING: No users found in database")
        else:
            # Show first few usernames
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

def admin_content(request):
    # Fetch all content types
    recipes = Recipe.objects.all().order_by('-created_at')
    posts = ForumPost.objects.all().order_by('-created_at')
    comments = Comment.objects.all().order_by('-created_at')
    resources = SharedResource.objects.all().order_by('-uploaded_at')

    context = {
        'recipes': recipes,
        'posts': posts,
        'comments': comments,
        'resources': resources
    }
    return render(request, 'admin_content.html', context)