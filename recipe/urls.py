from django.urls import path
from .views import (
    recipe_ai,
    recipe_generator, 
    kitchen_view, 
    display_recipe, 
    signup_view, 
    login_view, 
    logout_view,
    collection_view,
    likes_view,
    profile_view,
    diary_view,
    sharing_view,
    toggle_save_recipe,
    toggle_like_recipe,
    update_recipe,
    edit_recipe_view,
)

urlpatterns = [
    path("recipe_ai/", recipe_ai, name="recipe_ai"),
    path("generate/", recipe_generator, name="generate_recipe"),
    path("kitchen/", kitchen_view, name="kitchen"),
    path("recipe/<int:recipe_id>/", display_recipe, name="display_recipe"),
    path("recipe/<int:recipe_id>/save/", toggle_save_recipe, name="toggle_save_recipe"),
    path("recipe/<int:recipe_id>/like/", toggle_like_recipe, name="toggle_like_recipe"),
    path("recipe/<int:recipe_id>/update/", update_recipe, name="update_recipe"),
    path("recipe/<int:recipe_id>/edit/", edit_recipe_view, name="edit_recipe"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("collection/", collection_view, name="collection"),
    path("likes/", likes_view, name="likes"),
    path("profile/", profile_view, name="profile"),
    path("diary/", diary_view, name="diary"),
    path("sharing/", sharing_view, name="sharing"),
 
]
