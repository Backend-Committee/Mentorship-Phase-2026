import re
import uuid
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Lower


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"


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


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name="expenses")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="expenses")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_expenses")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=500, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "expenses"
        indexes = [
            models.Index(fields=["panel", "date"]),
            models.Index(fields=["panel", "category"]),
            models.Index(fields=["panel", "created_by"]),
        ]

    def clean(self) -> None:
        if self.amount <= Decimal("0"):
            raise ValidationError({"amount": "Amount must be greater than zero."})
        if self.category_id and self.panel_id and self.category.panel_id != self.panel_id:
            raise ValidationError({"category": "Category must belong to the same panel."})


class Budget(models.Model):
    class Period(models.TextChoices):
        MONTHLY = "monthly", "Monthly"
        QUARTERLY = "quarterly", "Quarterly"
        ANNUAL = "annual", "Annual"
        CUSTOM = "custom", "Custom"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="budgets",
    )
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    period = models.CharField(max_length=20, choices=Period.choices)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    alert_threshold = models.PositiveSmallIntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "budgets"
        constraints = [
            models.UniqueConstraint(
                fields=["panel", "category", "period", "start_date", "end_date"],
                name="uq_budget_period_scope",
            ),
        ]

    def clean(self) -> None:
        if self.limit_amount <= Decimal("0"):
            raise ValidationError({"limit_amount": "Budget limit must be greater than zero."})

        if self.category_id and self.panel_id and self.category.panel_id != self.panel_id:
            raise ValidationError({"category": "Category must belong to the same panel."})

        if self.period == self.Period.CUSTOM:
            if not self.start_date or not self.end_date:
                raise ValidationError("Custom period requires start_date and end_date.")
        elif self.start_date or self.end_date:
            raise ValidationError("start_date and end_date are only valid for custom period.")

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("start_date cannot be after end_date.")


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


class NotificationPreference(models.Model):
    class Delivery(models.TextChoices):
        IN_APP = "in_app", "In-App"
        EMAIL = "email", "Email"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_preferences")
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name="notification_preferences")
    type = models.CharField(max_length=30, choices=Notification.Type.choices)
    enabled = models.BooleanField(default=True)
    delivery = models.CharField(max_length=20, choices=Delivery.choices, default=Delivery.IN_APP)

    class Meta:
        db_table = "notification_preferences"
        constraints = [
            models.UniqueConstraint(fields=["user", "panel", "type"], name="uq_user_panel_notification_type"),
        ]


class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name="invitations")
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True)
    role = models.CharField(max_length=20, choices=PanelUser.Role.choices, default=PanelUser.Role.VIEWER)
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_invitations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="accepted_invitations")

    class Meta:
        db_table = "invitations"

    def __str__(self) -> str:
        return f"Invite {self.email} to {self.panel.name} ({self.role})"
