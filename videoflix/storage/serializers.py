from rest_framework import serializers
from storage.models import uploadMovie



class PreviewSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for previewing uploaded movies.
    This serializer specifies the fields to be included when previewing uploaded movies.
    """
    class Meta:
        model = uploadMovie
        fields = ['created_at','movie_name','cover','description_short','big_picture','random_key','genre','convert_status']

class MovieSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for full details of uploaded movies.
    This serializer specifies the fields to be included when displaying full details of uploaded movies.
    """
    class Meta:
        model = uploadMovie
        fields = ['movie_name','description_short','description','author','date_from','genre','video_length','age_rating','big_picture','video','movie_check','short_movie_check','upload_visible_check']



