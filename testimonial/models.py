from django.db import models


class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.rating})"

# Create your models here.
