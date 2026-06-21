from django.conf import settings
from django.db import models


class BodyMeasurement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='measurements')
    date = models.DateField()
    body_fat_percent = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    muscle_mass_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    muscle_mass_percent = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    bmi = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    water_percent = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    visceral_fat = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    bone_mass_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    basal_metabolism_kcal = models.PositiveIntegerField(null=True, blank=True)
    body_age = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    protein_percent = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    subcutaneous_fat_percent = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    source_analysis = models.ForeignKey(
        'analysis.AnalysisResult',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='measurements',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Measurement for {self.user.email} on {self.date}'

    class Meta:
        db_table = 'body_measurements'
        ordering = ('-date', '-created_at')
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
