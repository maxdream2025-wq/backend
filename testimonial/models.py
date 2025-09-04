from django.db import models


class Testimonial(models.Model):
    APPROVAL_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    name = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    approval_status = models.CharField(max_length=10, choices=APPROVAL_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True, help_text="Admin notes for approval/rejection")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.rating}) - {self.approval_status}"

# Create your models here.
