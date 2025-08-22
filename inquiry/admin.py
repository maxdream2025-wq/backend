from django.contrib import admin
from .models import PropertyInquiry


@admin.register(PropertyInquiry)
class PropertyInquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'property', 'created_at')
    list_filter = ('created_at', 'property')
    search_fields = ('full_name', 'email', 'property__property_name')
    readonly_fields = ('created_at',)
