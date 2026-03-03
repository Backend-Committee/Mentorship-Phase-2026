from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100 , blank=False , null=False)
    National_ID = models.CharField(max_length=20 , unique=True)
    email = models.EmailField(blank=False , null=False)
    phone = models.CharField(max_length=20 , blank=False , null=False)
    date_of_birth = models.DateField(blank=False , null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"