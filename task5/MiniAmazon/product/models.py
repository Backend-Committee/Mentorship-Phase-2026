from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    stock = models.IntegerField()
    is_Available = models.BooleanField(default=True)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)


# Create your models here.
