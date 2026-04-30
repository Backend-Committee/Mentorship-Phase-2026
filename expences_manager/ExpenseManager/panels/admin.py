from django.contrib import admin
from .models import Panel, PanelUser, Category


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
