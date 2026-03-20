from django.test import TestCase
from users.models import User
from users.serializers import UserRegistrationSerializer, UserSerializer

class UserSerializerTest(TestCase):
    def test_user_registration_serializer_valid(self):
        data = {
            'username': 'newuser',
            'password': 'strong_password_123',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(user.check_password('strong_password_123'))
        self.assertEqual(user.email, 'test@example.com')

    def test_user_registration_serializer_missing_fields(self):
        data = {
            'username': 'newuser',
            # Missing password
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_user_serializer_read_only_fields(self):
        # Role should be read-only in UserSerializer
        user = User.objects.create_user(username='user', password='password', role=User.Role.CUSTOMER)
        data = {
            'role': User.Role.ADMIN
        }
        serializer = UserSerializer(user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        # Role should NOT change
        self.assertEqual(updated_user.role, User.Role.CUSTOMER)
