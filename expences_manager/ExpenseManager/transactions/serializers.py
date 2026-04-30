from decimal import Decimal
from rest_framework import serializers

from .models import Expense, Budget


class ExpenseSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

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

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user
        return super().create(validated_data)


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
        read_only_fields = ["id", "created_by", "created_at", "budget_status"]

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
