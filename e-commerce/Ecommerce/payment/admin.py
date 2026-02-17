from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'method', 'status', 'created_at')
    list_filter = ('status', 'method', 'created_at')
