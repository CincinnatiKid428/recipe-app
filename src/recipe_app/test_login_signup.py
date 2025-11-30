from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

#Import models, views, forms
from .views import login_view, register_view
from .forms import CustomUserCreationForm

# Create your tests here.

#=== Login User View Tests ==============================================

class TestLoginView(TestCase):
    print(' ✔️ TestLoginView')

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            password='CorrectPassword!'
        )

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    def test_successful_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'tester',
            'password': 'CorrectPassword!',
        })

        self.assertRedirects(response, reverse('recipes:list'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'tester',
            'password': 'wrongpass',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertIsNotNone(response.context['error_message'])

    def test_missing_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertIsNotNone(response.context['error_message'])

    #=== Register User View Tests ==============================================

class TestRegisterView(TestCase):
    print(' ✔️ TestRegisterView')

    def test_register_view_get(self):
        """GET request should render the registration page."""
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')

        # Ensure form is CustomUserCreationForm
        self.assertIn('form', response.context)

    def test_user_can_register_successfully(self):
        """Valid POST should create the user and log them in."""
        payload = {
            'username': 'newuser',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        }

        response = self.client.post(reverse('register'), payload)

        # Successful registration redirects
        self.assertRedirects(response, reverse('recipes:list'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_register_duplicate_username_shows_error(self):
        """Submitting a username already in use should return a field-level error."""
        User.objects.create_user(username='existing', password='testpass')

        response = self.client.post(reverse('register'), {
            'username': 'existing',
            'password1': 'Password123!',
            'password2': 'Password123!',
        })

        self.assertEqual(response.status_code, 200)

        # View places errors into field_errors dict
        self.assertIn('username', response.context['field_errors'])
        self.assertGreater(len(response.context['field_errors']['username']), 0)

    def test_password_mismatch_shows_error(self):
        """Different password1/password2 should produce non-field errors."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'Password123!',
            'password2': 'Different987!',
        })

        self.assertEqual(response.status_code, 200)

        #Print form errors for debugging
        #print("⚠️ Form Errors:", response.context['form'].errors)

        #Ensure there are errors for the 'password2' field (mismatch error will generate in password2 field's error list)
        self.assertIn('password2', response.context['field_errors'])
        self.assertGreater(len(response.context['field_errors']['password2']), 0)

    def test_password_too_short_shows_error(self):
        """Ensures Django's UserCreationForm validation works with custom form."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': '123',
            'password2': '123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('password2', response.context['field_errors'])

    def test_password_entirely_numeric_shows_error(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': '123456789',
            'password2': '123456789',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('password2', response.context['field_errors'])