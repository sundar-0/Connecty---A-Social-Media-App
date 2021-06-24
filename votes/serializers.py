from .models import Vote
from rest_framework import serializers

class VoteSerializer(serializers.ModelSerializer):
    up_vote_by = serializers.ReadOnlyField(source='up_vote_by.username')
    down_vote_by=serializers.ReadOnlyField(source='down_vote_by.username')
    class Meta:
        model = Vote
        fields = ['id','post','up_vote_by','down_vote_by']


