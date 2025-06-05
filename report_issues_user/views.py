from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import IssueReport

@method_decorator(login_required, name='dispatch')
class ReportIssueView(View):
    template_name = 'reportIssues_user.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # 1. Extract form data
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')
        screenshot = request.FILES.get('screenshot')

        # 2. Debug prints (you can remove these later)
        print("POST received:", request.POST, request.FILES.keys())
        print("Creating IssueReport:", issue_type, description, "screenshot:", bool(screenshot))

        # 3. Validation
        if not issue_type or not description:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, self.template_name)

        if screenshot:
            if screenshot.size > 5 * 1024 * 1024:
                messages.error(request, 'File size must be less than 5MB.')
                return render(request, self.template_name)

            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if screenshot.content_type not in allowed_types:
                messages.error(request, 'Please upload a valid image file (JPG, PNG, GIF).')
                return render(request, self.template_name)

        try:
            # 4. REPLACE THIS ENTIRE TRY BLOCK WITH THE NEW CODE:
            IssueReport.objects.create(
                user=request.user,
                issue_type=issue_type,
                description=description,
                screenshot=screenshot if screenshot else None,
                status='open'
            )
            # messages.success(request, 'Thank you for reporting! We will review your issue shortly.')
            return render(request, self.template_name, {'success': True})

        except Exception as e:
            messages.error(request, f'An error occurred while submitting your report: {e}')
            return render(request, self.template_name)