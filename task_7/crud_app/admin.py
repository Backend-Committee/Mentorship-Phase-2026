from django.contrib import admin
from .models import *

models = (Person, Customer, Staff)
admin.site.register(models)