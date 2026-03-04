
from django.db import models

# Create your models here.

class Bank(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BankAdmin(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class BankAccount(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    card = models.ForeignKey('Card', on_delete=models.CASCADE)
class Card(models.Model):
    card_number = models.CharField(max_length=16, unique=True)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)
    networkProvider = models.CharField(max_length=20)
    card_holder_name = models.CharField(max_length=50)
