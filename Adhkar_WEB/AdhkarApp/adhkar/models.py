from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Adhkar(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='adhkar_list')
    title = models.CharField(max_length=255)
    content = models.TextField()
    points_value = models.IntegerField(default=1) 

    def __str__(self):
        return self.title