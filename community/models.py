from django.db import models
from django.contrib.auth.models import User

class DonationFoodPost(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donation_food_posts')
    food_name = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=[
        ('Fruits', 'Fruits'),
        ('Vegetables', 'Vegetables'),
        ('Dairy', 'Dairy'),
        ('Grains & Bread', 'Grains & Bread'),
        ('Protein', 'Protein & Meat'),
        ('Prepared Meals', 'Prepared Meals'),
        ('Canned Goods', 'Canned Goods'),
        ('Other', 'Other'),
    ])
    image = models.ImageField(upload_to='donation_food_posts/')
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Available', 'Available'),
        ('Claimed', 'Claimed'),
        ('Completed', 'Completed')
    ], default='Available')

    def __str__(self):
        return f"{self.food_name} by {self.donor.username}"

class ClaimedFood(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]
    
    food_post = models.ForeignKey(DonationFoodPost, on_delete=models.CASCADE, related_name='claims')
    claimer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claimed_foods')
    claimed_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f"{self.food_post.food_name} claimed by {self.claimer.username}"
