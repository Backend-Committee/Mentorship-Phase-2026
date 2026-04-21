from django.db import models
from sales.models import Invoice
from shifts.models import Shift
# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, unique=True)
    total_debt = models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return self.name


class CustomerDebts(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)

    def __str__(self):
        return f"invoice {self.invoice.id} for {self.customer.name} "


class DebtPayment(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete= models.RESTRICT)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} payed {self.amount} in {self.payment_date}"




