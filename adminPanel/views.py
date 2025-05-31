from django.contrib.auth.models import User
from django.shortcuts import render

def admin_dashboard(request):
    # Count the number of users
    total_users = User.objects.count()
    ## context = {
    ##    "total_users": total_users,
    ## } 

    print(f"Total Users: {total_users}")  # Check the console for the total user count
    
    return render(request, "adminPage.html", {'total_users': total_users})

def admin_user(request):
    users = User.objects.all()
    total_users = users.count()
    return render(request, "adminUser.html", {"users": users, "total_users": total_users})