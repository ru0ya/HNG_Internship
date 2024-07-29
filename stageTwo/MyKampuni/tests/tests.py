from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from kampuni.models import User


class AuthTests(APITestCase):
    """
    def setUp(self):
        User.objects.all().delete()
    """
    def register_user(self):
        url = reverse('register')
        data = {
                "first_name": "John",
                "last_name": "Doe",
                "email": "testdevru0ya@gmail.com",
                "password": "password123.",
                "phone": "123456789"
                }
        return self.client.post(url, data, format='json')

    def test_register_user(self):
        response = self.register_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("Registration succesful:", response.data)

    def test_login_user(self):
        register_response = self.register_user()
        self.assertEqual(
                register_response.status_code,
                status.HTTP_201_CREATED
                )

        url = reverse('login')
        data = {
                "email": "testdevru0ya@gmail.com",
                "password": "password123."
                }
        response = self.client.post(url, data, format='json')
        print("Login Response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIN('data', response.data)
        self.assertIn('accessToken', response.data['data'])

    def test_protected_endpoint(self):
        register_response = self.register_user()
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        url = reverse('login')
        data = {
                "email": "testdevru0ya@gmail.com",
                "password": "password123."
                }

        response = self.client.post(url, data, format='json')
        print("Login Response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        token = response.data['data']['accessToken']

        user_id = response.data['data']['user']['user_id']
        url = reverse('user-detail', kwargs={'user_id': user_id})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer' + token)
        response = self.client.get(url)
        print("Protected Endpoint Response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def tearDown(self):
        User.objects.all().delete()
