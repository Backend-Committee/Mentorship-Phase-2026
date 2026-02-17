from django.db import models

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='carts')
    cartitems = models.ManyToManyField('CartItem', related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username} - Created at {self.created_at}"
    
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.cartitems.all())


    def add_product(self, product, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        self.cartitems.add(cart_item)
        self.save()
    
    def remove_product(self, product):
        cart_item = self.cartitems.filter(product=product).first()
        if cart_item:
            self.cartitems.remove(cart_item)
            cart_item.delete()
            self.save()

    def clear_cart(self):
        self.cartitems.clear()
        self.save()


class CartItem(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
