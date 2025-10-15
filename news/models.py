from django.db import models
from django.utils import timezone
from urllib.parse import urlparse

class Article(models.Model):
    title = models.CharField(max_length=500)
    html_content = models.TextField()
    text_content = models.TextField()
    source_url = models.URLField(unique=True)
    source_domain = models.CharField(max_length=255, db_index=True, blank=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.source_url and not self.source_domain:
            self.source_domain = urlparse(self.source_url).netloc
        if not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.source_domain})"
