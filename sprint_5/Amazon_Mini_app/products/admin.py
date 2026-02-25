from django.contrib import admin
from .models import Product, Category

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'quantity', 'available']
    list_editable = ['price', 'category', 'available']
    search_fields = ['title']
    list_filter = ['category', 'available']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

