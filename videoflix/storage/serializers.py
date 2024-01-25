from rest_framework import serializers
from storage.models import uploadMovie



class PreviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = uploadMovie
        fields = ['created_at','movie_name','cover','description_short','big_picture','random_key','genre']

class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = uploadMovie
        fields = ['movie_name','description_short','description','author','date_from','genre','video_length','age_rating','big_picture','video']



