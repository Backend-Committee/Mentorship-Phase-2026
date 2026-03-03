from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(
        default=dict,
        blank=True
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"

