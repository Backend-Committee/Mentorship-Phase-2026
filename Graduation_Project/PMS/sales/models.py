from django.db import models
from inventory.models import Medicine
from shifts.models import Shift
# Create your models here.

class Invoice(models.Model):
    TYPE_CHOICES = (
        ('Sale', 'Sale'),
        ('Return', 'Return'),
    )
    PAYMENT_CHOICES = (
        ('Cash', 'Cash'),
        ('E-wallet', 'E-Wallet'),
        ('Debt', 'Debt'),
    )
    shift = models.ForeignKey(Shift, on_delete=models.RESTRICT, related_name='invoices')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='Cash')
    created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Sale')

    def __str__(self):
        return f"Invoice {self.id} - {self.type}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('invoice', 'medicine')

    def __str__(self):
        return f"Item: {self.medicine.name} in Invoice {self.invoice.id}"
