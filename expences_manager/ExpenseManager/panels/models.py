import re
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower

from accounts.models import User


class Panel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_panels")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "panels"

    def __str__(self) -> str:
        return self.name


class PanelUser(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        EDITOR = "editor", "Editor"
        VIEWER = "viewer", "Viewer"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="panel_memberships")
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=Role.choices)
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_panel_invitations",
    )
    joined_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "panel_users"
        constraints = [
            models.UniqueConstraint(fields=["user", "panel"], name="uq_panel_user"),
        ]

    def __str__(self) -> str:
        return f"{self.user.username} in {self.panel.name} ({self.role})"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    color_hex = models.CharField(max_length=7, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "categories"
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "panel",
                name="uq_category_name_panel_ci",
            ),
        ]

    def clean(self) -> None:
        if self.color_hex and not re.fullmatch(r"^#[0-9A-Fa-f]{6}$", self.color_hex):
            raise ValidationError({"color_hex": "Must be a valid hex color like #1A2B3C."})

    def __str__(self) -> str:
        return self.name
