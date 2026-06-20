from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model matching the SQL schema with email as unique identifier."""

    id = models.BigAutoField(primary_key=True)
    username = models.CharField(_("username"), max_length=100, blank=False)
    email = models.EmailField(_("email address"), max_length=255, unique=True, blank=False)
    is_doctor = models.BooleanField(_("doctor status"), default=False)
    is_lab_admin = models.BooleanField(_("lab admin status"), default=False)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

class Doctor(models.Model):
    """Doctor profile linked to User."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="user_id",
        related_name="doctor_profile",
    )
    specialization = models.CharField(_("specialization"), max_length=255, blank=True, null=True)

    class Meta:
        db_table = "doctors"
        verbose_name = _("doctor")
        verbose_name_plural = _("doctors")

    def __str__(self):
        return f"Doctor: {self.user.email}"


class LabAdmin(models.Model):
    """Lab Admin profile linked to User."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="user_id",
        related_name="lab_admin_profile",
    )

    lab = models.OneToOneField("facilities.Laboratory", on_delete=models.CASCADE, related_name="lab_admins")


    class Meta:
        db_table = "lab_admins"
        verbose_name = _("lab admin")
        verbose_name_plural = _("lab admins")

    def __str__(self):
        return f"Lab Admin: {self.user.email}"
