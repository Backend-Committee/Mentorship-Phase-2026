from django.db import models

from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BankAccount(models.Model):
    # ACCOUNT_TYPES = [('savings', 'Savings'), ('checking', 'Checking')]

    customer     = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='accounts')
    # account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='savings')
    balance      = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Account #{self.id} — {self.customer}"


class Transaction(models.Model):
    TRANSACTION_TYPES = [('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ('transfer', 'Transfer')]

    account    = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    type       = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount     = models.DecimalField(max_digits=12, decimal_places=2)
    to_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name='incoming_transfers')
    timestamp  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} — {self.amount}"