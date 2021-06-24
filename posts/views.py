
from .serializers import PostSerializer
from .models import Post
from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from user_profile.permissions import IsOwnerOrReadOnly
from rest_framework import status, viewsets
class PostViewSet(viewsets.ModelViewSet):
    """
    Posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
