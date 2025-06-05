from django.db import models
from django.contrib.auth.models import User

class IssueReport(models.Model):
    ISSUE_TYPES = [
        ('bug', 'Bug Report'),
        ('inappropriate', 'Inappropriate Content'),
        ('feature', 'Feature Request'),
        ('performance', 'Performance Issue'),
        ('accessibility', 'Accessibility Issue'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('resolved', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_reported_issues')
    issue_type = models.CharField(max_length=32, choices=ISSUE_TYPES, default='other')  # Added default here
    description = models.TextField(null=True, blank=True)
    screenshot = models.ImageField(upload_to='issue_screenshots/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')  # Keep only this line, remove the duplicate
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_issue_type_display()} by {self.user or 'Anonymous'}"