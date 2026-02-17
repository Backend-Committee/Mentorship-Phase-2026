from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'owner', 'category', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'created_at')
