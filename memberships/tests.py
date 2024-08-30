from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.utils import json

#tests
#I ran these with 'python manage.py test'
class RegistrationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.registration_url = reverse('register')

    def test_valid_registration(self):
        response = self.client.post(self.registration_url, json.dumps({
            'username': 'newuser',
            'password1': 'ValidPassword123',
            'password2': 'ValidPassword123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_password_mismatch(self):
        response = self.client.post(self.registration_url, json.dumps({
            'username': 'newuser',
            'password1': 'ValidPassword123',
            'password2': 'InvalidPassword123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_username_exists(self):
        User.objects.create_user('existinguser', 'password')
        response = self.client.post(self.registration_url, json.dumps({
            'username': 'existinguser',
            'password1': 'AnotherValidPassword123',
            'password2': 'AnotherValidPassword123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        User.objects.create_user('testuser', 'test@example.com', 'testpassword')

    def test_successful_login(self):
        response = self.client.post(self.login_url, json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        # Test login with wrong password
        response = self.client.post(self.login_url, json.dumps({
            'username': 'testuser',
            'password': 'wrongpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)


class HomepageViewTests(TestCase):
    def test_homepage_view(self):
        # Test rendering of homepage
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')