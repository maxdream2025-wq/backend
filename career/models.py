from django.db import models

class CareerApplication(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    country_code = models.CharField(max_length=10, default="+971")
    phone = models.CharField(max_length=20)
    cv_resume = models.FileField(upload_to='career_applications/', null=True, blank=True)
    description = models.TextField(blank=True)
    applied_for = models.CharField(max_length=100, default="Real Estate Agent")
    status = models.CharField(
        max_length=20, 
        choices=[
            ('pending', 'Pending Review'),
            ('reviewed', 'Reviewed'),
            ('shortlisted', 'Shortlisted'),
            ('rejected', 'Rejected'),
            ('hired', 'Hired')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Career Application'
        verbose_name_plural = 'Career Applications'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def cv_file_name(self):
        """Get just the filename without path"""
        if self.cv_resume:
            return self.cv_resume.name.split('/')[-1]
        return None
