from django.contrib import admin
from .models import CareerApplication

@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'applied_for', 'status', 'phone', 'cv_file_name', 'get_cv_download_link', 'created_at']
    list_filter = ['status', 'applied_for', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'cv_file_name']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'country_code', 'phone')
        }),
        ('Application Details', {
            'fields': ('applied_for', 'description', 'cv_resume')
        }),
        ('Status & Timestamps', {
            'fields': ('status', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_cv_download_link(self, obj):
        if obj.cv_resume:
            return f'<a href="/api/v1/career/download-cv/{obj.id}/" target="_blank">Download CV</a>'
        return 'No CV uploaded'
    get_cv_download_link.short_description = 'CV Download'
    get_cv_download_link.allow_tags = True
    
    actions = ['mark_reviewed', 'mark_shortlisted', 'mark_rejected', 'mark_hired']
    
    def mark_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
    mark_reviewed.short_description = "Mark selected applications as reviewed"
    
    def mark_shortlisted(self, request, queryset):
        queryset.update(status='shortlisted')
    mark_shortlisted.short_description = "Mark selected applications as shortlisted"
    
    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = "Mark selected applications as rejected"
    
    def mark_hired(self, request, queryset):
        queryset.update(status='hired')
    mark_hired.short_description = "Mark selected applications as hired"
