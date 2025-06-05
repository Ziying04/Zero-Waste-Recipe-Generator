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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    issue_type = models.CharField(max_length=32, choices=ISSUE_TYPES)
    description = models.TextField()
    screenshot = models.ImageField(upload_to='issue_screenshots/', null=True, blank=True)
    status = models.CharField(max_length=20, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_issue_type_display()} by {self.user or 'Anonymous'}"
