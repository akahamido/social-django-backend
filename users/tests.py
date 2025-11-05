from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {"email": "test@example.com", "password": "123456"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_login_user(self):
        user = User.objects.create_user(email="test2@example.com", password="123456")
        url = reverse('login')
        data = {"identifier": "test2@example.com", "password": "123456"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
