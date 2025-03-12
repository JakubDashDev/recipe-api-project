"""Views for the Tag API"""

from rest_framework import viewsets

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from tag import serializers

class TagViewSet(viewsets.ModelViewSet):
    """View for manage Tag APIs"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive recipes"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
      """Create new recipe"""
      serializer.save(user=self.request.user)