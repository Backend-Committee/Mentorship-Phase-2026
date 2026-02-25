from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True, default='no description.')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
    available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)
    # category = models.CharField(max_length=50, choices= categories, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.title
