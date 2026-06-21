from django.conf import settings
from django.db import models


class ExtractionTask(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='extractions')
    image = models.ImageField(upload_to='extractions/%Y/%m/%d/')
    extracted_text = models.TextField(blank=True, default='')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Extraction #{self.pk} by {self.user.email} ({self.status})'

    class Meta:
        db_table = 'extraction_tasks'
        ordering = ('-created_at',)
