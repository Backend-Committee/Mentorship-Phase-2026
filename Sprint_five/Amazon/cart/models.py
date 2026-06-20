from django.db import models

from main.models import Product

# Create your models here.
class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title}"