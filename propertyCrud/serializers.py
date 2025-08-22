from rest_framework import serializers
from .models import PropertyCategory, Property
from django.utils.text import slugify

class PropertyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyCategory
        fields = '__all__'
        read_only_fields = ['slug']  # slug is auto-generated

    def create(self, validated_data):
        # Generate base slug from title
        base_slug = slugify(validated_data['title'])
        slug = base_slug
        i = 1

        # Ensure slug is unique
        while PropertyCategory.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{i}"
            i += 1

        validated_data['slug'] = slug
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Optional: update slug if title changes
        if 'title' in validated_data:
            base_slug = slugify(validated_data['title'])
            slug = base_slug
            i = 1
            while PropertyCategory.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            validated_data['slug'] = slug
        return super().update(instance, validated_data)


class PropertySerializer(serializers.ModelSerializer):
    # Use nested serializer for read
    category = PropertyCategorySerializer(read_only=True)

    # Allow writing using category_id
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=PropertyCategory.objects.all(),
        source="category",
        write_only=True
    )

    class Meta:
        model = Property
        fields = '__all__'
