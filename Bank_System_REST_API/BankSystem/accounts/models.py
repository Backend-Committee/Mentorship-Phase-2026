from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    account_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Account Number')
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Balance')
    )
    is_frozen = models.BooleanField(
        default=False,
        verbose_name=_('Is Frozen')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"

