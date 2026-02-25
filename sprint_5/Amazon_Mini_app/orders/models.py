from django.db import models
from django.conf import settings
from django.db.models import ManyToManyField
from users.models import User
from products.models import Product


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.DateTimeField(auto_now_add=True)
    products = ManyToManyField(Product, through='OrderItem')
    completed = models.BooleanField(default=False)
    @property
    def total_price(self):
        items = self.orderitem_set.all()
        total = sum([item.item_total_price for item in items if item.item_total_price])
        return total



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.price == 0.00:
            self.price = self.product.price
        super().save(*args, **kwargs)
    @property
    def item_total_price(self):
        return self.product.price * self.quantity
