from rest_framework import serializers
from .models import News
from django.utils.text import slugify
from django.db import models

class NewsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['slug']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def create(self, validated_data):
        # Generate base slug from title
        base_slug = slugify(validated_data.get('title', ''))
        
        # If no order specified, set it to the next available order
        if 'order' not in validated_data or validated_data['order'] is None:
            max_order = News.objects.aggregate(models.Max('order'))['order__max'] or 0
            validated_data['order'] = max_order + 1
        
        # Generate unique slug
        validated_data['slug'] = self.generate_unique_slug(base_slug)
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Generate unique slug if title changed
        if 'title' in validated_data and validated_data['title'] != instance.title:
            base_slug = slugify(validated_data['title'])
            validated_data['slug'] = self.generate_unique_slug(base_slug)
        
        return super().update(instance, validated_data)

    def generate_unique_slug(self, base_slug):
        slug = base_slug
        i = 1
        while News.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{i}"
            i += 1
        return slug

    def validate_image(self, value):
        if value:
            # Check file size (5MB limit)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image file size must be under 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("Only JPEG, PNG, GIF, and WebP images are allowed.")
        
        return value
