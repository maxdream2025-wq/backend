from rest_framework import serializers
from django.conf import settings
from django.core.files.base import ContentFile
import os
import urllib.request
from .models import PropertyCategory, Property
from django.utils.text import slugify
from django.db import models

class PropertyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyCategory
        fields = '__all__'
        read_only_fields = ['slug']  # slug is auto-generated

    def create(self, validated_data):
        # Generate base slug from title
        base_slug = slugify(validated_data.get('title', ''))
        
        # If no order specified, set it to the next available order
        if 'order' not in validated_data or validated_data['order'] is None:
            max_order = PropertyCategory.objects.aggregate(models.Max('order'))['order__max'] or 0
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

        # Ensure slug is unique
        while PropertyCategory.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{i}"
            i += 1

        return slug


class PropertySerializer(serializers.ModelSerializer):
    # Use nested serializer for read
    category = PropertyCategorySerializer(read_only=True)

    # Allow writing using category_id
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=PropertyCategory.objects.all(),
        source="category",
        write_only=True
    )

    # Allow setting gallery via direct path when using JSON (Postman)
    property_gallery_path = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Property
        fields = '__all__'
        extra_fields = ['property_gallery_path']

    def to_internal_value(self, data):
        # Accept either an uploaded file in 'property_gallery' OR a string path
        # If client sends 'property_gallery' as a string, remap to 'property_gallery_path'
        try:
            mutable_data = data.copy()
        except Exception:
            mutable_data = data

        pg_val = mutable_data.get('property_gallery') if isinstance(mutable_data, dict) else None
        if isinstance(pg_val, str) and pg_val:
            if isinstance(mutable_data, dict):
                mutable_data['property_gallery_path'] = pg_val
                mutable_data.pop('property_gallery', None)

        ret = super().to_internal_value(mutable_data)
        path_value = (mutable_data.get('property_gallery_path')
                      if isinstance(mutable_data, dict) else None)
        if path_value is not None:
            ret['property_gallery_path'] = path_value
        return ret

    def create(self, validated_data):
        # If a direct path is provided and no uploaded file, set name directly
        gallery_path = validated_data.pop('property_gallery_path', None)
        if gallery_path and not validated_data.get('property_gallery'):
            file_obj = self._resolve_gallery_from_path(gallery_path)
            if isinstance(file_obj, ContentFile):
                # Downloaded file from URL
                validated_data['property_gallery'] = file_obj
            elif isinstance(file_obj, str):
                # Existing file inside MEDIA_ROOT or relative path
                validated_data['property_gallery'] = file_obj
            else:
                raise serializers.ValidationError({'property_gallery_path': 'File not found or could not be fetched.'})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        gallery_path = validated_data.pop('property_gallery_path', None)
        if gallery_path is not None and not validated_data.get('property_gallery'):
            # Allow clearing by empty string
            if gallery_path == "":
                validated_data['property_gallery'] = None
            else:
                file_obj = self._resolve_gallery_from_path(gallery_path)
                if isinstance(file_obj, ContentFile):
                    validated_data['property_gallery'] = file_obj
                elif isinstance(file_obj, str):
                    validated_data['property_gallery'] = file_obj
                else:
                    raise serializers.ValidationError({'property_gallery_path': 'File not found or could not be fetched.'})
        return super().update(instance, validated_data)

    def _resolve_gallery_from_path(self, path_value: str):
        """Return either ContentFile (for remote URL) or relative media path string.
        - If HTTP/HTTPS URL: download and return ContentFile with a safe name.
        - If starts with MEDIA_URL: strip and return relative path string.
        - If absolute filesystem path: if exists under any path, return relative path under MEDIA_ROOT/properties/ and move/copy is not handled here. Prefer MEDIA-relative path.
        - Else treat as relative to MEDIA_ROOT; if exists, return as-is; else, attempt to use as name (will 404 if not present).
        """
        val = path_value.strip()
        if not val:
            return None

        # Remote URL download
        if val.startswith('http://') or val.startswith('https://'):
            try:
                with urllib.request.urlopen(val) as resp:
                    data = resp.read()
                filename = os.path.basename(urllib.request.urlparse(val).path) or 'image.jpg'
                return ContentFile(data, name=f"properties/{filename}")
            except Exception:
                return None

        # If starts with MEDIA_URL, convert to relative storage name
        media_url = getattr(settings, 'MEDIA_URL', '/media/') or '/media/'
        if val.startswith(media_url):
            return val[len(media_url):]

        # Absolute filesystem path
        if os.path.isabs(val):
            if os.path.exists(val):
                # Store relative to MEDIA_ROOT/properties/<basename>
                basename = os.path.basename(val)
                return f"properties/{basename}"
            return None

        # Relative path inside MEDIA_ROOT
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        if media_root:
            abs_candidate = os.path.join(media_root, val)
            if os.path.exists(abs_candidate):
                return val

        # Fallback: return relative name; it may not exist yet
        return val
