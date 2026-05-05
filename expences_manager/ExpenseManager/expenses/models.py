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


class ReportSchedule(models.Model):
    class ReportType(models.TextChoices):
        SUMMARY = "summary", "Summary"
        MONTHLY = "monthly", "Monthly"
        TRENDS = "trends", "Trends"

    class ExportFormat(models.TextChoices):
        CSV = "csv", "CSV"
        PDF = "pdf", "PDF"
        XLSX = "xlsx", "XLSX"

    class Frequency(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name="report_schedules")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_report_schedules")
    report_type = models.CharField(max_length=20, choices=ReportType.choices)
    export_format = models.CharField(max_length=10, choices=ExportFormat.choices)
    frequency = models.CharField(max_length=20, choices=Frequency.choices)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="report_schedules",
    )
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    next_run_at = models.DateTimeField()
    last_run_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "report_schedules"
        indexes = [
            models.Index(fields=["panel", "is_active", "next_run_at"]),
        ]

    def clean(self) -> None:
        if self.report_type != self.ReportType.TRENDS and self.category_id:
            raise ValidationError({"category": "category is only allowed for trends reports."})

        if self.report_type == self.ReportType.TRENDS and self.category_id and self.category.panel_id != self.panel_id:
            raise ValidationError({"category": "Category must belong to the same panel."})

        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise ValidationError("date_from cannot be after date_to.")


class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = "create", "Create"
        UPDATE = "update", "Update"
        DELETE = "delete", "Delete"
        ACCEPT = "accept", "Accept"
        INVITE = "invite", "Invite"
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        PASSWORD_RESET = "password_reset", "Password Reset"
        CHANGE_ROLE = "change_role", "Change Role"
        RUN_SCHEDULE = "run_schedule", "Run Schedule"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    panel = models.ForeignKey(Panel, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    action = models.CharField(max_length=30, choices=Action.choices)
    entity_type = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_logs"
        indexes = [
            models.Index(fields=["panel", "created_at"]),
            models.Index(fields=["actor", "created_at"]),
            models.Index(fields=["action", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.action} {self.entity_type}:{self.entity_id}"


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


class Webhook(models.Model):
    class Events(models.TextChoices):
        EXPENSE_CREATED = "expense.created", "Expense Created"
        EXPENSE_UPDATED = "expense.updated", "Expense Updated"
        EXPENSE_DELETED = "expense.deleted", "Expense Deleted"
        BUDGET_EXCEEDED = "budget.exceeded", "Budget Exceeded"
        PANEL_INVITATION = "panel.invitation", "Panel Invitation"
        REPORT_RUN = "report.run", "Report Run"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name="webhooks")
    name = models.CharField(max_length=200)
    url = models.URLField()
    # store a list of event strings that this webhook subscribes to
    events = models.JSONField(default=list)
    secret = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    failure_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "webhooks"
        indexes = [
            models.Index(fields=["panel", "is_active"]),
        ]

    def __str__(self) -> str:
        return f"Webhook {self.name} -> {self.url}"


class RecurringExpense(models.Model):
    class Frequency(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        BIWEEKLY = "biweekly", "Bi-weekly"
        MONTHLY = "monthly", "Monthly"
        QUARTERLY = "quarterly", "Quarterly"
        ANNUAL = "annual", "Annual"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name="recurring_expenses")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="recurring_expenses")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_recurring_expenses")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=500, blank=True)
    frequency = models.CharField(max_length=20, choices=Frequency.choices)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_created_at = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recurring_expenses"
        indexes = [
            models.Index(fields=["panel", "is_active"]),
        ]

    def clean(self) -> None:
        if self.amount <= Decimal("0"):
            raise ValidationError({"amount": "Amount must be greater than zero."})
        if self.category_id and self.panel_id and self.category.panel_id != self.panel_id:
            raise ValidationError({"category": "Category must belong to the same panel."})
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError("start_date cannot be after end_date.")

    def __str__(self) -> str:
        return f"{self.description or self.amount} - {self.frequency}"
