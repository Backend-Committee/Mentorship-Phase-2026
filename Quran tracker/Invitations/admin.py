from django.contrib import admin

# Register your models here.
from .models import Invitation

admin.site.register(Invitation)