from django.db import models

from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Availability(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='availability')
    blocked_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)