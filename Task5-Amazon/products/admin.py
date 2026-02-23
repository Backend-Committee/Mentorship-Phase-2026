from django.contrib import admin

from products.models import Product, Category
from cart.models import Cart

# Register your models here.
# Superuser
# name: Rawan
# password: task5amazon

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_available', 'category']  # columns shown in the list
    list_filter = ['category', 'is_available']  # filter sidebar on the right
    search_fields = ['name', 'description']  # search bar at the top
    list_editable = ['price', 'stock', 'is_available']  # edit directly from the list without opening each product
    ordering = ['-price'] 
    list_per_page = 20 
    readonly_fields = ['created_at'] 

# admin.site.register(Product, ProductAdmin)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
# admin.site.register(Category, CategoryAdmin)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'total_price']
# admin.site.register(Cart,CartAdmin)