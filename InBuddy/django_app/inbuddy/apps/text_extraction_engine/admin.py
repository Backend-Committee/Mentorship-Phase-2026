from django.contrib import admin

from .models import ExtractionTask


@admin.register(ExtractionTask)
class ExtractionTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'extracted_text')
    readonly_fields = ('extracted_text', 'error_message', 'created_at', 'updated_at')
