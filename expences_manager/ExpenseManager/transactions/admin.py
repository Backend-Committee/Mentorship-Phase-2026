from django.contrib import admin
from .models import Expense, Budget


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "panel", "category", "amount", "date", "created_by", "deleted_at")
    list_filter = ("date", "deleted_at")


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("id", "panel", "category", "period", "limit_amount", "alert_threshold")
    list_filter = ("period",)
