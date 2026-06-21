from django.contrib import admin

from .models import BodyMeasurement


@admin.register(BodyMeasurement)
class BodyMeasurementAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'body_fat_percent', 'bmi', 'weight_kg', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('user__email', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
