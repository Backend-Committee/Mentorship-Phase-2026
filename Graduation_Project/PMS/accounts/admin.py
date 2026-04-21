from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Pharmacy Info', {'fields': ('phone', 'role', 'hourly_rate', 'worked_hours')}),
    )
    list_display = ('username', 'role', 'phone', 'is_staff')
admin.site.register(User, MyUserAdmin)
