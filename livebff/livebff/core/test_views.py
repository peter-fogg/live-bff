from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from datetime import date
from urllib.parse import urljoin

from livebff.core.models import Profile

class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="test_user", password="pw")
        self.user.refresh_from_db()
        self.user.profile.full_name = "Test User"

    def test_home_redirect(self):
        """Unauthenticated users are redirected to log in."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, urljoin(reverse('login'), '?next=/'))

    def test_home(self):
        """Authenticated users are greeted by name."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("You're home, Test User!", response.content.decode('utf-8'))

    def test_signup_unauthenticated(self):
        """Renders a signup form if the user is unauthenticated."""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].errors, {})

    def test_signup_authenticated(self):
        """If authenticated, the user is redirected to home."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_signup_success(self):
        """
        On a successful signup a User and Profile object are created, the
        user is logged in, and they are redirected to home.
        """
        birth_date = '01/01/1980'
        signup_form = {
            'full_name': 'Anthony Fauci',
            'username': 'afauci',
            'password1': 'cdc123!!',
            'password2': 'cdc123!!',
            'birth_date': birth_date
        }
        response = self.client.post(reverse('signup'), signup_form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))
        user = User.objects.get(username='afauci')
        self.assertEqual(user.profile.birth_date, date(year=1980, month=1, day=1))

    def test_signup_error(self):
        """Without a valid form returns the same page with errors."""
        response = self.client.post(reverse('signup'), {'full_name': 'foo'}) # missing some fields
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['form'].errors), 0)
