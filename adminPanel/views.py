from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Recipe, Donation, ForumPost, Comment, SharedResource

# def admin_dashboard(request):
    # Count the number of users
  #  total_users = User.objects.count()
    ## context = {
    ##    "total_users": total_users,
    ## } 

   # print(f"Total Users: {total_users}")  # Check the console for the total user count
    
    #return render(request, "adminPage.html", {'total_users': total_users})

def admin_dashboard(request):
    total_users = User.objects.count()
    context = {
        'total_users': total_users,
    }
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