from .models import Vote
from django.shortcuts import render
from rest_framework import permissions, status, viewsets
from . serializers import VoteSerializer
from posts.models import Post
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . permissions import hasSelfVotedOrReadOnly
# Create your views here.
class VoteViewSet(viewsets.ModelViewSet):
    """
    Votes
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,hasSelfVotedOrReadOnly]
    def perform_create(self, serializer):
        post_instance= get_object_or_404(Post, pk=self.request.data['post'])
        if self.request.data['up_vote']:
            print(Vote.objects.filter(post=post_instance,up_vote_by=self.request.user).exists())

            if Vote.objects.filter(post=post_instance,up_vote_by=self.request.user).exists():
                return Response({"message":"You have already liked the post"})
            else:
                serializer.save(up_vote_by=self.request.user,post=post_instance)  
                
        elif self.request.data['down_vote']:

            if Vote.objects.filter(post=post_instance,down_vote_by=self.request.user).exists():
                return Response({"message":"You have already liked the post"})
            else:    
                serializer.save(down_vote_by=self.request.user,post=post_instance)
           
           
        
        

  
  
  
  


