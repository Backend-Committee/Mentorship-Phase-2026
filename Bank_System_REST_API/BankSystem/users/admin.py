from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = list(UserAdmin.fieldsets) + [
        (None, {'fields': ('role',)}),
    ]
    add_fieldsets = list(UserAdmin.add_fieldsets) + [
        (None, {'fields': ('role',)}),
    ]
    list_display = list(UserAdmin.list_display) + ['role']
    list_filter = list(UserAdmin.list_filter) + ['role']
