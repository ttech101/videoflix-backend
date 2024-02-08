import os
import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils.crypto import get_random_string

# Create your models here.
class uploadMovie(models.Model):
    """
    Model representing uploaded movies.
    Attributes:
        user (ForeignKey): The user who uploaded the movie.
        created_at (DateField): The date when the movie was uploaded.
        last_play (DateTimeField): The date and time when the movie was last played.
        movie_name (str): The name of the movie.
        description_short (str): A short description of the movie.
        description (str): A detailed description of the movie.
        author (str): The author of the movie.
        date_from (DateField): The release date of the movie.
        video_length (str): The length of the movie.
        genre (str): The genre of the movie.
        movie_check (bool): Flag indicating if it's a movie.
        short_movie_check (bool): Flag indicating if it's a short movie.
        nature_check (bool): Flag indicating if it's a nature documentary.
        funny_check (bool): Flag indicating if it's a funny movie.
        knowledge_check (bool): Flag indicating if it's an educational movie.
        other_check (bool): Flag indicating if it belongs to other categories.
        age_rating (int): The age rating of the movie.
        upload_visible_check (bool): Flag indicating if the upload is visible.
        cover (ImageField): The cover image of the movie.
        big_picture (ImageField): The big picture associated with the movie.
        video (FileField): The video file of the movie.
        random_key (UUIDField): A unique identifier for the movie.
        automatic_cover (bool): Flag indicating if cover is automatically generated.
        automatic_image (bool): Flag indicating if image is automatically generated.
        convert_status (int): The conversion status of the movie.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=datetime.today)
    last_play = models.DateTimeField(null=True, blank=True)
    movie_name = models.CharField(max_length=255,null=True, blank=True)
    description_short = models.CharField(max_length=250,null=True, blank=True)
    description = models.CharField(max_length=1000,null=True, blank=True)
    author = models.CharField(max_length=100,null=True, blank=True)
    date_from = models.DateField(null=True)
    video_length= models.CharField(max_length=20,null=True, blank=True)
    genre = models.CharField(max_length=100,null=True, blank=True)
    movie_check = models.BooleanField(default=False)
    short_movie_check = models.BooleanField(default=False)
    nature_check = models.BooleanField(default=False)
    funny_check = models.BooleanField(default=False)
    knowledge_check = models.BooleanField(default=False)
    other_check = models.BooleanField(default=False)
    age_rating = models.PositiveIntegerField(default=0)
    upload_visible_check = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='cover/', default='static/load-142_256.gif',null=True, blank=True)
    big_picture = models.ImageField(upload_to='big_picture/', null=True, blank=True)
    video = models.FileField(upload_to='video/', null=True, blank=True)
    random_key  = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    automatic_cover = models.BooleanField(default=False)
    automatic_image = models.BooleanField(default=False)
    convert_status = models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        """
        Custom save method to generate a random key if it's a new instance.
        Args:
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.
        """
        if not self.pk:
            self.random_key = uuid.uuid4()
        super().save(*args, **kwargs)


