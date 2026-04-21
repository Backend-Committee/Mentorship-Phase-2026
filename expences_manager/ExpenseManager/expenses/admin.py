from django.contrib import admin

from .models import Budget, Category, Expense, Notification, Panel, PanelUser, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "created_at")
    search_fields = ("username", "email")


@admin.register(Panel)
class PanelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "created_at")
    search_fields = ("name", "owner__username", "owner__email")


@admin.register(PanelUser)
class PanelUserAdmin(admin.ModelAdmin):
    list_display = ("user", "panel", "role", "joined_at")
    list_filter = ("role",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "panel", "is_default", "created_at")
    list_filter = ("is_default",)
    search_fields = ("name",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "panel", "category", "amount", "date", "created_by", "deleted_at")
    list_filter = ("date", "deleted_at")


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("id", "panel", "category", "period", "limit_amount", "alert_threshold")
    list_filter = ("period",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "user", "panel", "is_read", "created_at")
    list_filter = ("type", "is_read")
