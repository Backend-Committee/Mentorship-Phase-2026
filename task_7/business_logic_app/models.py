from django.db import models
from crud_app.models import Account

class Transaction(models.Model):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"
    INTEREST_ADDITION = "INTEREST_ADDITION"
    TRANSACTION_TYPES = {
        DEPOSIT: "Deposit",
        WITHDRAWAL: "Withdrawal",
        TRANSFER: "Transfer",
        INTEREST_ADDITION: "Interest Addition",
    }
    
    account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, related_name="transaction_main_set")
    to_account = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True, related_name="transaction_to_set")
    amount = models.PositiveIntegerField()
    type = models.CharField(choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction {self.id}"
