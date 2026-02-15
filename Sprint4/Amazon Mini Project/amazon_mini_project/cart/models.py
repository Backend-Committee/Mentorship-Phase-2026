from django.db import models

from user.models import User


class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="items",  # better naming
    )
    product = models.ForeignKey(
        "catalog.Product", on_delete=models.CASCADE, related_name="cart_items"
    )

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    class Meta:
        unique_together = ("user", "product")
