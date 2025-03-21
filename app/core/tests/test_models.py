"""
Tests for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email='user@example.com', password='password123'):
    """Create and return sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating user with an email is success"""
        email = "test@test.com"
        password = "pass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test emails is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email(self):
        """Test creating user without an email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'pass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test createing recipe is successful"""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "testpassword123"
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title="Test",
            time_minutes=5,
            price=Decimal('5.50'),
            description="Test description"
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating tag is successful"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)