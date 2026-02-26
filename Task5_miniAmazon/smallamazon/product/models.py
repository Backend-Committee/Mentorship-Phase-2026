from django.db import models
from django.core.validators import MinValueValidator

class product(models.Model):
    categories = [('Tea','Tea'), ('coffee','coffee'), ('Juice','Juice'),('Folwers','Folwers'),('Laptop','Laptop'),('Fruit','Fruit'),('LipGloss','LipGloss')]
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    category = models.CharField(max_length=50, choices=categories)
    image = models.ImageField(upload_to='product_images/%y/%m/%d', blank=True)
    Is_Available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)