from rest_framework import serializers
from account.models import UserModel, UserProfile

class UserModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the UserModel model.
    This serializer specifies the fields to be included when serializing UserModel instances.
    """
    class Meta:
        model = UserModel
        fields = ['first_name','email']

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the UserProfile model.
    This serializer specifies the fields to be included when serializing UserProfile instances.
    """
    class Meta:
        model = UserProfile
        fields = ['avatar','automatic_playback','language']
