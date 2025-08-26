from django.db import models
from django.utils.text import slugify

class News(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to="news/", null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    feature = models.BooleanField(default=False)  # <-- Added field

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            slug_candidate = base_slug
            i = 1
            while News.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{i}"
                i += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
