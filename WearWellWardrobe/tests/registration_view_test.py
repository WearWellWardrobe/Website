from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from WearWellWardrobe.models import Category, Page, UserProfile

class RegisterViewTests(TestCase):
    """
    Tests for the register() view.
    """
    def setUp(self):
        self.client = Client()

    def test_register_get(self):
        """
        GET should show the register form.
        """
        response = self.client.get(reverse('WearWellWardrobe:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIn('user_form', response.context)
        self.assertIn('profile_form', response.context)

    def test_register_post_valid(self):
        """
        POST valid data should create a user and profile, then show 'registered=True'.
        """
        post_data = {
            'username': 'newuser',
            'password': 'testpass123',
            'email': 'test@example.com',
        }
        response = self.client.post(reverse('WearWellWardrobe:register'), post_data)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['registered'])


class UserLoginTests(TestCase):
    """
    Tests for the user_login() view.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='loginuser', password='loginpass')

    def test_user_login_valid(self):
        """
        POST valid credentials should log in and redirect to home.
        """
        post_data = {
            'username': 'loginuser',
            'password': 'loginpass',
        }
        response = self.client.post(reverse('WearWellWardrobe:login'), post_data)
        self.assertRedirects(response, reverse('WearWellWardrobe:home'))

    def test_user_login_invalid(self):
        """
        Invalid credentials should return an error message and re-render login.
        """
        post_data = {
            'username': 'wronguser',
            'password': 'wrongpass',
        }
        response = self.client.post(reverse('WearWellWardrobe:login'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('messages', response.cookies)