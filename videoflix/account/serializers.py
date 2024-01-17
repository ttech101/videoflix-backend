from rest_framework import serializers
from account.models import UserProfile



class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar','automatic_playback','language']