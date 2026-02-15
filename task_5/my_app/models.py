from django.db import models

# Application working feature
# Admin Feature - basic but manual and not safe
# Admin Feature - customized, safe, and automatic
# Filter feature
# Search Feature
# Date for product feature
# Tags feature

# Create your models here.
class Category(models.Model):
    name = models.CharField(unique=True)
    
    def __str__(self):
        return f"Category - {self.name}"
    
    class Meta:
        verbose_name_plural = "categories"



class Product(models.Model):
    name = models.CharField()
    desc = models.TextField(verbose_name="description", blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete = models.SET_NULL)
    price = models.IntegerField()
    stock = models.IntegerField()
    images_filenames = models.TextField(blank=True)
    
    def get_main_image_static_path(self):
        main_image_filename = self.images_filenames.split('\n')[0]
        return f"images/product_images/{self.id}/{main_image_filename}"
    
    def is_available(self):
        return self.stock > 0
    
    def __str__(this):
        return f"Product - {this.name}"
     
