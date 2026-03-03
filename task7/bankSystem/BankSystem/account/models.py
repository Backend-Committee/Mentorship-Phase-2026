from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

    def get_absolute_url(self):
        return reverse('account-detail', args=[str(self.id)])

    class Meta:
        ordering = ['account_number']

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
    )

    sender = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='sent_transactions',
        null=True,
        blank=True
    )

    receiver = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='received_transactions',
        null=True,
        blank=True
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)