from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

class UserViewTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role=User.Role.ADMIN)
        self.manager_user = User.objects.create_user(username='manager', password='password', role=User.Role.MANAGER)
        self.customer_user = User.objects.create_user(username='customer', password='password', role=User.Role.CUSTOMER)
        self.register_url = reverse('auth_register') 
        self.list_url = reverse('office-users-list')

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'password': 'StrongPass123!',
            'email': 'new@example.com'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_list_users_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_as_manager(self):
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_as_customer_forbidden(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_unauthenticated_unauthorized(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
