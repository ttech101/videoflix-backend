from rest_framework import serializers
from storage.models import uploadMovie



class PreviewSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for previewing uploaded movies.
    This serializer specifies the fields to be included when previewing uploaded movies.
    Attributes:
        created_at (DateField): The date when the movie was uploaded.
        movie_name (str): The name of the movie.
        cover (ImageField): The cover image of the movie.
        description_short (str): A short description of the movie.
        big_picture (ImageField): The big picture associated with the movie.
        random_key (UUIDField): A unique identifier for the movie.
        genre (str): The genre of the movie.
        convert_status (int): The conversion status of the movie.
    """
    class Meta:
        model = uploadMovie
        fields = ['created_at','movie_name','cover','description_short','big_picture','random_key','genre','convert_status']

class MovieSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for full details of uploaded movies.
    This serializer specifies the fields to be included when displaying full details of uploaded movies.
    Attributes:
        movie_name (str): The name of the movie.
        description_short (str): A short description of the movie.
        description (str): A detailed description of the movie.
        author (str): The author of the movie.
        date_from (DateField): The release date of the movie.
        genre (str): The genre of the movie.
        video_length (str): The length of the movie.
        age_rating (int): The age rating of the movie.
        big_picture (ImageField): The big picture associated with the movie.
        video (FileField): The video file of the movie.
        movie_check (bool): Flag indicating if it's a movie.
        short_movie_check (bool): Flag indicating if it's a short movie.
        upload_visible_check (bool): Flag indicating if the upload is visible.
    """
    class Meta:
        model = uploadMovie
        fields = ['movie_name','description_short','description','author','date_from','genre','video_length','age_rating','big_picture','video','movie_check','short_movie_check','upload_visible_check']



