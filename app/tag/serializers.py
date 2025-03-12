"""Seriazliers for the Tags API view"""

from rest_framework import serializers
from core.models import Tag

class TagSerializer(serializers.ModelSerializer):
    """Seriazlier for Tag object"""

    class Meta:
        model = Tag
        fields = [
            'id',
            'name'
        ]
        read_only_fields = ['id']