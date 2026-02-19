from django.db import models
class Category(models.Model):

    name = models.CharField(max_length= 50)

    def __str__(self):
        return self.name


class Product(models.Model):

    name  = models.CharField(max_length= 50)
    price = models.DecimalField(max_digits= 10 , decimal_places= 2)
    description = models.TextField(max_length= 1000)
    category = models.ForeignKey(Category , on_delete= models.CASCADE)
    image = models.ImageField(upload_to='products/images/%y/%m/%d')
    available = models.BooleanField(default= True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'