from django.contrib import admin

from .models import AnalysisResult


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'extraction_task', 'analyzed_at')
    list_filter = ('analyzed_at',)
    search_fields = ('user__email', 'source_text')
    readonly_fields = ('parsed_metrics', 'source_text', 'analyzed_at')
