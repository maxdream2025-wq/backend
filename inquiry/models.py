from django.db import models
from propertyCrud.models import Property


class PropertyInquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Property Inquiries'

    def __str__(self):
        return f"Inquiry from {self.full_name} for {self.property.property_name}"
