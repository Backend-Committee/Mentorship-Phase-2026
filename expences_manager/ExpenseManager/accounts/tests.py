from django.test import TestCase
from django.conf import settings

from .models import User


class AccountsModelsTest(TestCase):
    def test_auth_user_model_setting(self):
        self.assertEqual(settings.AUTH_USER_MODEL, "accounts.User")

    def test_user_meta(self):
        self.assertEqual(User._meta.db_table, "users")
        email_field = User._meta.get_field("email")
        self.assertTrue(email_field.unique)
