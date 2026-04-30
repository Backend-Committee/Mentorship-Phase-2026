import uuid
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from panels.models import Panel, Category
from accounts.models import User


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
        if self.category and self.panel and self.category.panel.id != self.panel.id:
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
                fields=["panel", "category", "period", "start_date"],
                name="uq_budget_period_scope",
            ),
        ]

    def clean(self) -> None:
        if self.limit_amount <= Decimal("0"):
            raise ValidationError({"limit_amount": "Budget limit must be greater than zero."})

        if self.category and self.panel and self.category.panel.id != self.panel.id:
            raise ValidationError({"category": "Category must belong to the same panel."})

        if self.period == self.Period.CUSTOM:
            if not self.start_date or not self.end_date:
                raise ValidationError("Custom period requires start_date and end_date.")
        elif self.start_date or self.end_date:
            raise ValidationError("start_date and end_date are only valid for custom period.")

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("start_date cannot be after end_date.")

        if not 0 <= self.alert_threshold <= 100:
            raise ValidationError({"alert_threshold": "Must be between 0 and 100."})
