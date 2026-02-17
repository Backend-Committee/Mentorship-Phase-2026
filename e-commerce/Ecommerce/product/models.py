from django.db import models


STATIC_CATEGORIES = [
    ('electronics', 'Electronics'),
    ('fashion', 'Fashion'),
    ('home', 'Home & Garden'),
    ('books', 'Books'),
    ('toys', 'Toys & Games'),
    ('sports', 'Sports & Outdoors'),
    ('beauty', 'Beauty & Personal Care'),
    ('automotive', 'Automotive'),
    ('health', 'Health & Wellness'),
    ('grocery', 'Grocery & Gourmet Food'),
]

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='products')
    category = models.CharField(max_length=50, choices=STATIC_CATEGORIES)
    pic = models.ImageField(upload_to='product_images/', null=True, blank=True)

  