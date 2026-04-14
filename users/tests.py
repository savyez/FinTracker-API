# users/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.token_url = reverse('token')
        self.valid_payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPass123!',
        }

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_returns_tokens(self):
        response = self.client.post(self.register_url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', response.data)
        self.assertIn('access_token', response.data['data'])
        self.assertIn('refresh_token', response.data['data'])

    def test_register_duplicate_username(self):
        self.client.post(self.register_url, self.valid_payload)
        response = self.client.post(self.register_url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_password(self):
        payload = self.valid_payload.copy()
        del payload['password']
        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        User.objects.create_user(**self.valid_payload)
        response = self.client.post(self.token_url, {
            'username': self.valid_payload['username'],
            'password': self.valid_payload['password'],
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('access_token', response.data['data'])
        self.assertIn('refresh_token', response.data['data'])

    def test_login_wrong_password(self):
        User.objects.create_user(**self.valid_payload)
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)