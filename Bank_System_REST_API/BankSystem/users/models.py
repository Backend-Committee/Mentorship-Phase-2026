from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', _('Customer')
        TELLER = 'TELLER', _('Teller')
        MANAGER = 'MANAGER', _('Manager')
        ADMIN = 'ADMIN', _('Admin')
        AUDITOR = 'AUDITOR', _('Auditor')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
        verbose_name=_('Role')
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

