from django.contrib import admin

# Register your models here.
from .models import User, UserRoom

admin.site.register(User)
admin.site.register(UserRoom)