from django.db import models
from django.conf import settings
from accounts.models import Account
# Create your models here.

class Transaction(models.Model):
    class TransType(models.TextChoices):
        Deposit = "Deposit"
        Withdraw = "Withdraw"
        transfer = "Transfer"
    appointment = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account')
    type = models.CharField(choices=TransType.choices, default=TransType.Deposit, max_length=10)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transfer_to = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfer_to' )

    def __str__(self):
        return f"{self.account.user} - {self.type} - {self.id}"


