from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)


class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
