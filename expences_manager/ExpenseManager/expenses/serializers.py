import re
from decimal import Decimal

from rest_framework import serializers

from .models import (
    Budget,
    Category,
    Expense,
    Invitation,
    Notification,
    NotificationPreference,
    Panel,
    PanelUser,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_username(self, value: str) -> str:
        if not re.fullmatch(r"^[A-Za-z0-9_]{3,50}$", value):
            raise serializers.ValidationError(
                "Username must be 3-50 chars and use only letters, numbers, and underscores."
            )
        return value

    def validate_password(self, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must include at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must include at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must include at least one digit.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panel
        fields = ["id", "name", "owner", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class PanelUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanelUser
        fields = ["user", "panel", "role", "invited_by", "joined_at"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "panel", "name", "color_hex", "is_default", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        panel = attrs.get("panel") or getattr(self.instance, "panel", None)
        name = attrs.get("name") or getattr(self.instance, "name", None)
        if panel and name:
            qs = Category.objects.filter(panel=panel, name__iexact=name)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({"name": "Category name must be unique within panel."})

        color_hex = attrs.get("color_hex")
        if color_hex and not re.fullmatch(r"^#[0-9A-Fa-f]{6}$", color_hex):
            raise serializers.ValidationError({"color_hex": "Must be a valid hex color like #1A2B3C."})

        return attrs


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id",
            "panel",
            "category",
            "created_by",
            "amount",
            "date",
            "description",
            "deleted_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]

    def validate_amount(self, value):
        if value <= Decimal("0"):
            raise serializers.ValidationError("Amount must be greater than zero.")
        if value.as_tuple().exponent < -2:
            raise serializers.ValidationError("Amount can have at most two decimal places.")
        return value

    def validate(self, attrs):
        panel = attrs.get("panel") or getattr(self.instance, "panel", None)
        category = attrs.get("category") or getattr(self.instance, "category", None)

        if panel and category and category.panel_id != panel.id:
            raise serializers.ValidationError({"category": "Category must belong to the same panel."})

        return attrs


class BudgetSerializer(serializers.ModelSerializer):
    budget_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Budget
        fields = [
            "id",
            "panel",
            "category",
            "limit_amount",
            "period",
            "start_date",
            "end_date",
            "alert_threshold",
            "created_at",
            "budget_status",
        ]
        read_only_fields = ["id", "created_at", "budget_status"]

    def validate_limit_amount(self, value):
        if value <= Decimal("0"):
            raise serializers.ValidationError("Budget limit must be greater than zero.")
        return value

    def validate(self, attrs):
        panel = attrs.get("panel") or getattr(self.instance, "panel", None)
        category = attrs.get("category") if "category" in attrs else getattr(self.instance, "category", None)
        period = attrs.get("period") or getattr(self.instance, "period", None)
        start_date = attrs.get("start_date") if "start_date" in attrs else getattr(self.instance, "start_date", None)
        end_date = attrs.get("end_date") if "end_date" in attrs else getattr(self.instance, "end_date", None)

        if category and panel and category.panel_id != panel.id:
            raise serializers.ValidationError({"category": "Category must belong to the same panel."})

        if period == Budget.Period.CUSTOM:
            if not start_date or not end_date:
                raise serializers.ValidationError("Custom period requires start_date and end_date.")
        else:
            if start_date or end_date:
                raise serializers.ValidationError(
                    "start_date and end_date are only valid when period is custom."
                )

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("start_date cannot be after end_date.")

        threshold = attrs.get("alert_threshold")
        if threshold is not None and not 0 <= threshold <= 100:
            raise serializers.ValidationError({"alert_threshold": "Must be between 0 and 100."})

        qs = Budget.objects.filter(panel=panel, category=category, period=period)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists() and period != Budget.Period.CUSTOM:
            raise serializers.ValidationError(
                "Only one active budget is allowed for the same panel/category/period scope."
            )

        if qs.exists() and period == Budget.Period.CUSTOM and start_date and end_date:
            overlap_qs = qs.filter(start_date__lte=end_date, end_date__gte=start_date)
            if overlap_qs.exists():
                raise serializers.ValidationError(
                    "A custom budget already exists in an overlapping date range for this scope."
                )

        return attrs

    def get_budget_status(self, obj) -> str:
        return "on_track"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "user", "panel", "type", "message", "is_read", "created_at"]
        read_only_fields = ["id", "created_at"]


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ["id", "user", "panel", "type", "enabled", "delivery"]
        read_only_fields = ["id"]


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["id", "panel", "email", "token", "role", "invited_by", "created_at", "accepted_at", "accepted_by"]
        read_only_fields = ["id", "token", "created_at", "accepted_at", "accepted_by"]
