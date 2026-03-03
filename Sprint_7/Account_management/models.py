from django.db import models
from customer_Management.models import Customer

# Create your models here.
class Account(models.Model):
    customer = models.ForeignKey(Customer , on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20 , blank=False , null=False)
    balance = models.DecimalField(max_digits=10 , decimal_places=2 , blank=False , null=False, default=0)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.account_type}"

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"


class Transaction(models.Model):

    options = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer'),
    )
    account = models.ForeignKey(Account , on_delete=models.CASCADE , related_name='transactions')
    amount = models.DecimalField(max_digits=10 , decimal_places=2 , blank=False , null=False)
    transaction_type = models.CharField(max_length=20 , choices=options , blank=False , null=False)
    date = models.DateField(auto_now_add=True)
    target_account_id = models.ForeignKey(Account , on_delete=models.CASCADE ,
                                          related_name='target_transactions' , null=True , blank=True)

    def __str__(self):
        return f"{self.account.customer.name} - {self.account.account_type} - {self.amount}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"