from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from recipe.models import Recipe
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
            }, status=403)  # Changed to 403 Forbidden
        
        # Prevent users from deleting themselves
        if user_to_delete.id == request.user.id:
            return JsonResponse({
                'success': False,
                'error': 'You cannot delete your own account.'
            }, status=403)  # Changed to 403 Forbidden
        
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


def admin_content(request):
    print("=== ADMIN CONTENT VIEW CALLED ===")
    
    # Get current time for date calculations
    now = timezone.now()
    yesterday = now - timedelta(days=1)
    last_week = now - timedelta(days=7)
    last_month = now - timedelta(days=30)
    
    try:
        # PENDING REVIEW CONTENT
        # Assuming you have a status field or similar to identify content awaiting moderation
        pending_recipes = Recipe.objects.filter(
            Q(status='pending') | Q(is_approved=False)
        ).count() if hasattr(Recipe, 'status') or hasattr(Recipe, 'is_approved') else 0
        
        pending_comments = Comment.objects.filter(
            Q(status='pending') | Q(is_approved=False)
        ).count() if hasattr(Comment, 'status') or hasattr(Comment, 'is_approved') else 0
        
        pending_resources = SharedResource.objects.filter(
            Q(status='pending') | Q(is_approved=False)
        ).count() if hasattr(SharedResource, 'status') or hasattr(SharedResource, 'is_approved') else 0
        
        total_pending = pending_recipes + pending_comments + pending_resources
        
        # Calculate pending content from yesterday
        pending_yesterday = Recipe.objects.filter(
            created_at__gte=yesterday,
            created_at__lt=now
        ).count() if hasattr(Recipe, 'created_at') else 0
        
        print(f"Pending content: {total_pending} (recipes: {pending_recipes}, comments: {pending_comments}, resources: {pending_resources})")
        
        # PUBLISHED CONTENT
        published_recipes = Recipe.objects.filter(
            Q(status='published') | Q(is_approved=True)
        ).count() if hasattr(Recipe, 'status') or hasattr(Recipe, 'is_approved') else Recipe.objects.count()
        
        published_comments = Comment.objects.filter(
            Q(status='published') | Q(is_approved=True)
        ).count() if hasattr(Comment, 'status') or hasattr(Comment, 'is_approved') else Comment.objects.count()
        
        published_resources = SharedResource.objects.filter(
            Q(status='published') | Q(is_approved=True)
        ).count() if hasattr(SharedResource, 'status') or hasattr(SharedResource, 'is_approved') else SharedResource.objects.count()
        
        total_published = published_recipes + published_comments + published_resources
        
        # Calculate growth from last month
        published_last_month = Recipe.objects.filter(
            created_at__gte=last_month,
            created_at__lt=now - timedelta(days=30)
        ).count() if hasattr(Recipe, 'created_at') else 0
        
        published_growth = ((total_published - published_last_month) / max(published_last_month, 1)) * 100 if published_last_month > 0 else 0
        
        print(f"Published content: {total_published} (growth: {published_growth:.1f}%)")
        
        # REPORTED CONTENT
        # Assuming you have a reported field or similar
        reported_recipes = Recipe.objects.filter(
            is_reported=True
        ).count() if hasattr(Recipe, 'is_reported') else 0
        
        reported_comments = Comment.objects.filter(
            is_reported=True
        ).count() if hasattr(Comment, 'is_reported') else 0
        
        reported_resources = SharedResource.objects.filter(
            is_reported=True
        ).count() if hasattr(SharedResource, 'is_reported') else 0
        
        total_reported = reported_recipes + reported_comments + reported_resources
        
        # Calculate reported content from yesterday
        reported_yesterday = Comment.objects.filter(
            created_at__gte=yesterday,
            is_reported=True
        ).count() if hasattr(Comment, 'created_at') and hasattr(Comment, 'is_reported') else 0
        
        print(f"Reported content: {total_reported}")
        
        # TOTAL COMMENTS
        total_comments = Comment.objects.count()
        
        # Calculate comments growth from last week
        comments_last_week_count = Comment.objects.filter(
            created_at__lt=last_week
        ).count() if hasattr(Comment, 'created_at') else 0
        
        comments_growth = ((total_comments - comments_last_week_count) / max(comments_last_week_count, 1)) * 100 if comments_last_week_count > 0 else 0
        
        print(f"Total comments: {total_comments} (growth: {comments_growth:.1f}%)")
        
        # FETCH DETAILED CONTENT FOR TABLES
        
        # PENDING REVIEW CONTENT
        pending_review_items = []
        
        # Get pending recipes
        try:
            if hasattr(Recipe, 'status'):
                pending_recipes = Recipe.objects.filter(status='pending').select_related('author')
            elif hasattr(Recipe, 'is_approved'):
                pending_recipes = Recipe.objects.filter(is_approved=False).select_related('author')
            else:
                pending_recipes = Recipe.objects.all()[:5]  # Default to first 5 if no status field
                
            for recipe in pending_recipes:
                pending_review_items.append({
                    'id': recipe.id,
                    'title': getattr(recipe, 'title', getattr(recipe, 'name', 'Untitled Recipe')),
                    'author': recipe.author.username if hasattr(recipe, 'author') and recipe.author else 'Unknown',
                    'type': 'Recipe',
                    'type_badge': 'success',
                    'submitted': recipe.created_at if hasattr(recipe, 'created_at') else now,
                    'description': getattr(recipe, 'description', getattr(recipe, 'instructions', 'No description available'))[:80] + '...'
                })
        except Exception as e:
            print(f"Error fetching pending recipes: {e}")
        
        # Get pending comments
        try:
            if hasattr(Comment, 'status'):
                pending_comments = Comment.objects.filter(status='pending').select_related('author')
            elif hasattr(Comment, 'is_approved'):
                pending_comments = Comment.objects.filter(is_approved=False).select_related('author')
            else:
                # Fallback - get recent comments
                pending_comments = Comment.objects.all().order_by('-created_at')[:3]
                
            for comment in pending_comments:
                pending_review_items.append({
                    'id': comment.id,
                    'title': getattr(comment, 'content', getattr(comment, 'text', 'Comment'))[:50] + '...',
                    'author': comment.author.username if hasattr(comment, 'author') and comment.author else 'Unknown',
                    'type': 'Comment',
                    'type_badge': 'purple',
                    'submitted': comment.created_at if hasattr(comment, 'created_at') else now,
                    'description': getattr(comment, 'content', getattr(comment, 'text', 'No content available'))[:80] + '...'
                })
        except Exception as e:
            print(f"Error fetching pending comments: {e}")
        
        # Sort by submission time (most recent first)
        pending_review_items.sort(key=lambda x: x['submitted'], reverse=True)
        pending_review_items = pending_review_items[:20]  # Limit to 20 items
        
        # PUBLISHED CONTENT
        published_items = []
        
        try:
            # Get published recipes
            if hasattr(Recipe, 'status'):
                pub_recipes = Recipe.objects.filter(status='published').select_related('author')[:10]
            elif hasattr(Recipe, 'is_approved'):
                pub_recipes = Recipe.objects.filter(is_approved=True).select_related('author')[:10]
            else:
                pub_recipes = Recipe.objects.all()[:10]
                
            for recipe in pub_recipes:
                # Calculate engagement (likes + comments)
                likes_count = getattr(recipe, 'likes_count', getattr(recipe, 'likes', 0))
                comments_count = Comment.objects.filter(recipe=recipe).count() if hasattr(Comment, 'recipe') else 0
                
                published_items.append({
                    'id': recipe.id,
                    'title': getattr(recipe, 'title', getattr(recipe, 'name', 'Untitled Recipe')),
                    'author': recipe.author.username if hasattr(recipe, 'author') and recipe.author else 'Unknown',
                    'type': 'Recipe',
                    'type_badge': 'success',
                    'published': recipe.created_at if hasattr(recipe, 'created_at') else now,
                    'description': getattr(recipe, 'description', 'No description available')[:80] + '...',
                    'likes': likes_count,
                    'comments': comments_count
                })
        except Exception as e:
            print(f"Error fetching published recipes: {e}")
        
        try:
            # Get published comments
            if hasattr(Comment, 'status'):
                pub_comments = Comment.objects.filter(status='published').select_related('author')[:10]
            elif hasattr(Comment, 'is_approved'):
                pub_comments = Comment.objects.filter(is_approved=True).select_related('author')[:10]
            else:
                pub_comments = Comment.objects.all()[:10]
                
            for comment in pub_comments:
                likes_count = getattr(comment, 'likes_count', getattr(comment, 'likes', 0))
                comments_count = Comment.objects.filter(comment=comment).count() if hasattr(Comment, 'comment') else 0
                
                published_items.append({
                    'id': comment.id,
                    'title': getattr(comment, 'content', 'Comment')[:80] + '...',
                    'author': comment.author.username if hasattr(comment, 'author') and comment.author else 'Unknown',
                    'type': 'Comment',
                    'type_badge': 'purple',
                    'published': comment.created_at if hasattr(comment, 'created_at') else now,
                    'description': getattr(comment, 'content', 'No content available')[:80] + '...',
                    'likes': likes_count,
                    'comments': comments_count
                })
        except Exception as e:
            print(f"Error fetching published comments: {e}")
        
        published_items.sort(key=lambda x: x['published'], reverse=True)
        
        # REPORTED CONTENT
        reported_items = []
        
        try:
            # Get reported content
            if hasattr(Recipe, 'is_reported'):
                reported_recipes = Recipe.objects.filter(is_reported=True).select_related('author')
            else:
                reported_recipes = []
                
            for recipe in reported_recipes:
                reported_items.append({
                    'id': recipe.id,
                    'title': getattr(recipe, 'title', getattr(recipe, 'name', 'Untitled Recipe')),
                    'author': recipe.author.username if hasattr(recipe, 'author') and recipe.author else 'Unknown',
                    'type': 'Recipe',
                    'report_reason': getattr(recipe, 'report_reason', 'Inappropriate Content'),
                    'reported_by': getattr(recipe, 'reported_by', 'Anonymous'),
                    'reported_date': getattr(recipe, 'reported_date', recipe.created_at if hasattr(recipe, 'created_at') else now),
                    'description': getattr(recipe, 'description', 'No description available')[:80] + '...'
                })
        except Exception as e:
            print(f"Error fetching reported content: {e}")
        
        # If no reported content, add sample data for demonstration
        if not reported_items:
            reported_items = [
                {
                    'id': 999,
                    'title': 'Sample Reported Content',
                    'author': 'SampleUser',
                    'type': 'Recipe',
                    'report_reason': 'Inappropriate Content',
                    'reported_by': 'ModeratorUser',
                    'reported_date': now - timedelta(hours=2),
                    'description': 'This is sample reported content for demonstration purposes...'
                }
            ]
        
        print(f"Content fetched - Pending: {len(pending_review_items)}, Published: {len(published_items)}, Reported: {len(reported_items)}")
        
    except Exception as e:
        print(f"ERROR in admin_content view: {e}")
        # Set default values in case of error
        total_pending = pending_yesterday = 0
        total_published = published_growth = 0
        total_reported = reported_yesterday = 0
        total_comments = comments_growth = 0
        pending_review_content = []
    
    context = {
        # Dashboard statistics (for the overview cards)
        'pending_review_count': total_pending,
        'pending_review_change': pending_yesterday,
        'published_content_count': total_published,
        'published_content_growth': round(published_growth, 1),
        'reported_content_count': total_reported,
        'reported_content_change': reported_yesterday,
        'total_comments_count': total_comments,
        'comments_growth': round(comments_growth, 1),
        
        # Content for table displays
        'pending_review_items': pending_review_items,
        'published_items': published_items,
        'reported_items': reported_items,
        
        # Original content queries (for backward compatibility)
        'recipes': Recipe.objects.all().order_by('-created_at')[:50],
        'comments': Comment.objects.all().order_by('-created_at')[:50],
        'resources': SharedResource.objects.all().order_by('-uploaded_at')[:50] if hasattr(SharedResource.objects.first(), 'uploaded_at') else SharedResource.objects.all()[:50],
    }
    
    print(f"Context summary: Pending={total_pending}, Published={total_published}, Reported={total_reported}, Comments={total_comments}")
    print("=== END ADMIN CONTENT VIEW ===")
    
    return render(request, 'admin_content.html', context)