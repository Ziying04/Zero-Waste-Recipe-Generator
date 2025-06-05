from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from recipe.models import Recipe
from django.views.decorators.http import require_POST
from report_issues_user.models import IssueReport
from django.contrib import messages


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
    pass