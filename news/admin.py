from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'slug', 'feature', 'image_preview')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'desc')
    list_filter = ('date', 'feature')
    list_editable = ('feature',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'desc', 'date', 'slug')
        }),
        ('Media & Features', {
            'fields': ('image', 'feature'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; max-width: 100px; object-fit: cover; border: 1px solid #ddd; border-radius: 4px;" />'
        return "No Image"
    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True


