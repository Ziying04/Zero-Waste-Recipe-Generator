# report_issues_user/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import IssueReport

@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue_type', 'user', 'status', 'status_display', 'created_at', 'resolved_count_display')
    list_editable = ('status',)
    list_filter = ('status', 'issue_type', 'created_at')
    search_fields = ('description', 'user__username')
    actions = ['mark_resolved', 'mark_open']

    def status_display(self, obj):
        if obj.status == 'resolved':
            return format_html('<span style="color: green; font-weight: bold;">✓ Resolved</span>')
        else:
            return format_html('<span style="color: orange; font-weight: bold;">⏳ Open</span>')
    status_display.short_description = 'Visual Status'
    status_display.admin_order_field = 'status'

    def resolved_count_display(self, obj):
        count = IssueReport.objects.filter(status='resolved').count()
        return format_html('<span style="color: green; font-size: 12px;">Total Resolved: {}</span>', count)
    resolved_count_display.short_description = 'Resolution Stats'

    def mark_resolved(self, request, queryset):
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} issue(s) marked as resolved.')
    mark_resolved.short_description = 'Mark selected as resolved'

    def mark_open(self, request, queryset):
        updated = queryset.update(status='open')
        self.message_user(request, f'{updated} issue(s) marked as open.')
    mark_open.short_description = 'Mark selected as open'
