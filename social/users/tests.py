from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
import unittest

class UserTests(APITestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_user_registration(self):
        """
        Ensure we can register a new user.
        """
        url = reverse('user-list')  # This should resolve to /users/
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, 'newuser')

    # skip login tests until login views are implemented
    # @unittest.skip("Skipping login test until login is implemented")
    def test_user_login(self):
        """
        Ensure we can log in with valid credentials.
        """
        url = '/api-auth/login/'  # Directly using the built-in login endpoint provided by DRF
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @unittest.skip("Skipping login because in DRF have to be checked manually")
    def test_user_login_invalid_credentials(self):
        """
        Ensure we cannot log in with invalid credentials.
        """
        # Clear cookies to ensure no previous session remains
        self.client.logout()
        self.client.cookies.clear()

        # Try logging in with invalid credentials
        url = '/api-auth/login/'  # Directly using the built-in login endpoint provided by DRF
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')

        # Check if the response code is 200 (indicating that the form was reloaded)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response contains the login failure message or an error element
        self.assertContains(response, "Please enter a correct username and password", html=True)

    def test_user_profile(self):
        """
        Ensure a user can view their profile after logging in.
        """
        self.client.login(username='testuser', password='password123')
        url = reverse('user-detail', args=[self.user.id])  # Assuming you use a viewset
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
