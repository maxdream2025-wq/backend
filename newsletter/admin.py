from django.contrib import admin
from .models import Newsletter

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    list_filter = ['subscribed_at']
    search_fields = ['email']
    ordering = ['-subscribed_at']
    readonly_fields = ['subscribed_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-subscribed_at')
