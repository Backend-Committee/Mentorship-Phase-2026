from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):
    def test_create_user_with_default_role(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertEqual(user.role, User.Role.CUSTOMER)
        self.assertEqual(str(user), "testuser (Customer)")

    def test_create_user_with_specific_role(self):
        user = User.objects.create_user(
            username='adminuser',
            password='password123',
            role=User.Role.ADMIN
        )
        self.assertEqual(user.role, User.Role.ADMIN)
        self.assertEqual(str(user), "adminuser (Admin)")
