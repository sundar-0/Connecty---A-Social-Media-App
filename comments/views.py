from .models import Comment
from rest_framework import permissions
from user_profile.permissions import IsOwnerOrReadOnly
from rest_framework import status, viewsets

from . serializers import CommentSerializer


# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    """Comments"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

