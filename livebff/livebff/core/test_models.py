from django.contrib.auth.models import User
from django.test import TestCase

from livebff.core.models import Profile

class ProfileTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username="testuser")
        self.test_user.refresh_from_db()

    def test_is_active_default(self):
        """Profile objects are not active by default."""
        self.assertFalse(self.test_user.profile.is_active())

    def test_is_active(self):
        """With a full name and bio the user is active."""
        self.test_user.profile.bio = 'I am a robot.'
        self.test_user.profile.full_name = 'Test User'
        self.assertTrue(self.test_user.profile.is_active())
