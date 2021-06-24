from .models import UserProfile
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model=UserProfile
        fields='__all__'