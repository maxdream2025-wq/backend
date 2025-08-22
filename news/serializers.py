from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['slug']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Keep slug stable unless title is changed and slug not set manually
        if 'title' in validated_data and not validated_data.get('slug'):
            # Regenerate a unique slug based on new title
            from django.utils.text import slugify
            base_slug = slugify(validated_data['title'])
            slug_candidate = base_slug
            i = 1
            while News.objects.filter(slug=slug_candidate).exclude(pk=instance.pk).exists():
                slug_candidate = f"{base_slug}-{i}"
                i += 1
            validated_data['slug'] = slug_candidate
        return super().update(instance, validated_data)


