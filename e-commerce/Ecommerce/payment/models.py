from django.db import models

# Create your models here.


payment_methods = [
    ('credit_card', 'Credit Card'),
    ('paypal', 'PayPal'),
    ('bank_transfer', 'Bank Transfer'),
    ('cash_on_delivery', 'Cash on Delivery'),
]

class Payment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=payment_methods)
    status = models.CharField(max_length=20, default='pending') # can be 'pending', 'completed', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} - Status: {self.status}"
