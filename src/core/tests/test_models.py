"""
Tests for Models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email='test@example.com', password='password123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """"Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sampple_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sampple_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='sample123'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                password='sample123'
            )

    def test_create_superuser(self):
        """Test creating a suepruser."""
        user = get_user_model().objects.create_superuser(
            email="test@example.com",
            password="sample123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
