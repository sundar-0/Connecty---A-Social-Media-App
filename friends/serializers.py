from .models import FriendRequest
from rest_framework import serializers
from django.contrib.auth.models import User

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=FriendRequest
        fields=['request_from','request_to','status']