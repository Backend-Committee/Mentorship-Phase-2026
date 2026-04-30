import uuid
from django.db import models

from accounts.models import User
from panels.models import Panel


class Notification(models.Model):
    class Type(models.TextChoices):
        BUDGET_WARNING = "budget_warning", "Budget Warning"
        BUDGET_EXCEEDED = "budget_exceeded", "Budget Exceeded"
        PANEL_INVITATION = "panel_invitation", "Panel Invitation"
        SYSTEM = "system", "System"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=30, choices=Type.choices)
    message = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        indexes = [
            models.Index(fields=["user", "is_read"]),
        ]
