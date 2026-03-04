from django.contrib import admin

from banks.models import Bank, BankAccount, BankAdmin, Card

# Register your models here.
admin.site.register(Bank)
admin.site.register(BankAdmin)
admin.site.register(BankAccount)
admin.site.register(Card)
