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
    location_search = models.CharField(max_length=255)
    property_type = models.CharField(max_length=100)
    completion_date = models.CharField(max_length=50)
    payment_plan = models.CharField(max_length=50)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    property_gallery = models.ImageField(upload_to="properties/")
    property_type_search = models.JSONField(default=list)
    user_type = models.JSONField(default=list)
    bedroom = models.JSONField(default=list)
    bathroom = models.JSONField(default=list)
    area = models.JSONField(default=dict)
    status = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)  # allow null

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.property_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.property_name
