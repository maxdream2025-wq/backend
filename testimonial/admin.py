from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'rating', 'approval_status', 'created_at']
    list_filter = ['approval_status', 'rating', 'created_at']
    search_fields = ['name', 'email', 'text']
    readonly_fields = ['created_at']
    list_editable = ['approval_status']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('name', 'email', 'rating', 'text')
        }),
        ('Admin Management', {
            'fields': ('approval_status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
