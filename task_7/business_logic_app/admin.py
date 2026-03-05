from django.contrib import admin
from .models import Transaction

# Register your models here.
models = (Transaction)
admin.site.register(models)