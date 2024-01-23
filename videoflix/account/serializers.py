from rest_framework import serializers
from account.models import UserModel, UserProfile



class UserModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserModel
        fields = ['first_name','email']

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar','automatic_playback','language']
