from django.contrib import admin
from .models import News
from django.utils.html import mark_safe


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'feature', 'order', 'date', 'image_preview')
    list_filter = ('feature', 'date')
    list_editable = ('feature', 'order')
    search_fields = ('title', 'desc')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', '-date')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'desc', 'date', 'slug')
        }),
        ('Media & Display', {
            'fields': ('image', 'feature', 'order')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 50px; max-width: 50px;" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'


