from django.conf import settings
from django.db import models


class AnalysisResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analyses')
    extraction_task = models.ForeignKey(
        'text_extraction_engine.ExtractionTask',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='analyses',
    )
    source_text = models.TextField()
    parsed_metrics = models.JSONField(default=dict)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Analysis #{self.pk} for {self.user.email} on {self.analyzed_at}'

    class Meta:
        db_table = 'analysis_results'
        ordering = ('-analyzed_at',)
