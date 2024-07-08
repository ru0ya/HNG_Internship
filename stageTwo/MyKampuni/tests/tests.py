from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class AuthTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "password": "password123",
                "phone": "1234567890"
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        # register user
        self.test_register_user()
        # login
        url = reverse('login')
        data = {
                "email": "john@example.com",
                "password": "password123"
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_protected_endpoint(self):
        # register user
        self.test_register_user()
        # login with same user
        url = reverse('login')
        data = {
                "email": "john@example.com",
                "password": "password123"
                }
        response = self.client.post(url, data, format='json')
        token = response.data['data']['accessToken']

        # access protected endpoint
        url = reverse(
                'user-detail',
                kwargs={
                    'user_id': response.data['data']['user']['user_id']
                    }
                )
        self.client.credentials(HTTP_AUTHORIZATION='Bearer' + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
