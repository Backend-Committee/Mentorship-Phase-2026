from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    transaction = models.OneToOneField(
        'transactions.Transaction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    gateway = models.CharField(
        max_length=50,
        help_text=_('Payment Gateway Name')
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    payment_reference = models.CharField(
        max_length=100,
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_reference}: {self.amount} ({self.status})"

