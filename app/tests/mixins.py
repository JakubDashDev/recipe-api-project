from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse


class AuthRequiredMixin:
    """Mixin to test authentication requirment for API views"""

    def test_auth_required(self):
        res = self.client.get(self.API_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateSampleUserMixin:
    """Mixin to create sample user"""

    def create_user(self, email="test@example.com", password="testpass123", **extra_fields):
        return get_user_model().objects.create_user(email=email, password=password, **extra_fields)


def detail_url(url, id):
    """Mixin to create detail URL"""
    return reverse(url, args=[id])