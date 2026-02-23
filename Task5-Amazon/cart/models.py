from django.db import models
from django.core.validators import MinValueValidator

from products.models import Product
from django.db.models import F, Sum

class CartItem(models.Model):
    # id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # we can use the related name 'items' to access the cart items from the cart model, so we don't need to add a related name here
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    # unique_together = ('product', 'cart')
    # unique here won't work, i have to put it in class meta
    # quantity = models.IntegerField(min_value=1, default=1)
    quantity = models.IntegerField(default=1, validators = [MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # unique_together = ('product', 'cart')
        # the method below is the more advanced method 
        constraints = [
            models.UniqueConstraint(fields= ['product', 'cart'], name='unique_product_cart')
        ]
        verbose_name_plural = "Cart Items"
        ordering = ['-added_at']
        

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Cart (models.Model):
    # id = models.AutoField(primary_key=True)
    # a dummy field until we implement user authentication
    # user = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart of {self.user}"
    
    def total_price(self):
        total = 0
        # for item in self.items.all():
        #     total += item.product.price * item.quantity
        
        # this is supposed to calculate the sum in sql itself instead of sending all the rows to python then calculate it
        # F means field reference inside the sql database
        # it also is great in race conditions
        
        # aggregate returns one value, annotate edits in all rows
        # return self.items.aggregate(
        #     total = Sum(F('product__price') * F('quantity'))
        # )['total'][0]
        return self.items.aggregate(
            total=Sum(F('product__price') * F('quantity'))
        )['total'] or 0
