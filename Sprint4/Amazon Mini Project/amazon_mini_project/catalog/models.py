from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=250)
    sale_percent = models.IntegerField()
    category = models.ManyToManyField(Category, related_name="students")

    def __str__(self):
        return f"{self.title} - {self.category} -> {self.price}"
