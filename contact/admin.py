from django.contrib import admin
from .models import ContactSubmission

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'help_category', 'phone', 'submitted_at']
    list_filter = ['help_category', 'submitted_at']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    ordering = ['-submitted_at']
    readonly_fields = ['submitted_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'country_code', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('help_category', 'message')
        }),
        ('Timestamps', {
            'fields': ('submitted_at',),
            'classes': ('collapse',)
        }),
    )
