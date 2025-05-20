from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    id_recipe = models.CharField(max_length=10, unique=True, null=True)
    name = models.CharField(max_length=255)
    cooking_time = models.IntegerField()  # Cooking time in minutes
    steps = models.TextField()  # Steps for cooking
    image_url = models.URLField(max_length=500, blank=True, null=True)  # New field for image URL
    ingredients = models.TextField(default="Not specified")  # Provide a default value
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', null=True)
    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_recipes', blank=True)

    def __str__(self):
        return self.name

    def total_likes(self):
        return self.likes.count()

    def total_saves(self):
        return self.saved_by.count()

    def save(self, *args, **kwargs):
        if not self.id_recipe:
            # Generate recipe ID in format RCxxx
            last_recipe = Recipe.objects.order_by('-id').first()
            last_id = 1 if not last_recipe else int(last_recipe.id) + 1
            self.id_recipe = f'RC{last_id:03d}'
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.user.username

class RecipeLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.recipe.name}"

