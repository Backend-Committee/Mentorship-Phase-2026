from django.contrib import admin
from .models import Customer, CustomerDebts, DebtPayment
# Register your models here.

admin.site.register(Customer)
admin.site.register(CustomerDebts)
admin.site.register(DebtPayment)