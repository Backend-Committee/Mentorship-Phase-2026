from django.contrib import admin
from .models import product, login, Category

admin.site.register(product)
admin.site.register(login)
admin.site.register(Category)

