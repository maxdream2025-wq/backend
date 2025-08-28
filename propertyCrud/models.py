from django.db import models
from django.utils.text import slugify

class PropertyCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    property_category = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    developer = models.BooleanField(default=False)  # <-- Add this line

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Property(models.Model):
    category = models.ForeignKey(PropertyCategory, related_name="property", on_delete=models.CASCADE)
    property_name = models.CharField(max_length=255)
    property_sub_heading = models.CharField(max_length=255)
    property_desc = models.TextField()
    location = models.CharField(max_length=255)
    property_type = models.CharField(max_length=100)
    completion_date = models.CharField(max_length=50)
    payment_plan = models.CharField(max_length=50)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    property_gallery = models.ImageField(upload_to="properties/", blank=True, null=True)
    bedroom = models.CharField(max_length=255)
    bathroom = models.CharField(max_length=255)
    area = models.JSONField(default=dict)
    status = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.property_name:
            base_slug = slugify(self.property_name)
            slug_candidate = base_slug
            i = 1
            from .models import Property as PropertyModel
            while PropertyModel.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{i}"
                i += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.property_name
