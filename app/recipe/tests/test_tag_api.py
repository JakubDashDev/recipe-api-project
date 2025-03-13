"""Test for Tag API"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

from tests.mixins import AuthRequiredMixin, CreateSampleUserMixin, detail_url

TAG_URL = reverse("recipe:tag-list")


def detail_url(tag_id):
    """Create and return a Tag detail URL"""
    return reverse("recipe:tag-detail", args=[tag_id])


class PublicRecipeAPITests(TestCase, AuthRequiredMixin):
    """Test unauthenticated API requests"""

    # NOTE: AuthRequiredMixin checks for user authentication

    def setUp(self):
        self.client = APIClient()
        self.API_URL = TAG_URL


class PrivateTagAPITests(TestCase, CreateSampleUserMixin):
    """Test authenticate API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user()

        self.client.force_authenticate(self.user)

    def test_get_tags(self):
        """Test getting a list of tags"""
        Tag.objects.create(user=self.user, name="Sample")
        Tag.objects.create(user=self.user, name="Second")

        res = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by("-id")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_my_tags(self):
        """Test get Tags that belongs to user"""

        user2 = self.create_user(email="user@example.com")

        tag = Tag.objects.create(user=self.user, name="Sample")
        Tag.objects.create(user=user2, name="Second")

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)
        self.assertEqual(res.data[0]["id"], tag.id)

    def test_update_tag(self):
        """Test updating Tag by owner"""

        tag = Tag.objects.create(user=self.user, name="Sample")

        url = detail_url(tag.id)
        payload = {"name": "NewTag"}

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tag.refresh_from_db()
        self.assertEqual(tag.name, payload["name"])

    def test_deleting_tag(self):
        """Test deleting a Tag"""
        tag = Tag.objects.create(user=self.user, name="Sample")

        url = detail_url(tag.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(id=tag.id).exists())
