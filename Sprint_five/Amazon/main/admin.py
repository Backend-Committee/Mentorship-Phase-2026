from django.contrib import admin
import main.models as models

# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Banner)