from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class uploadMovie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='uploadMovie')
    created_at = models.DateField(default=datetime.today)
    last_play = models.DateTimeField(null=True, blank=True)
    movie_name = models.CharField(max_length=255,null=True, blank=True)
    description_short = models.CharField(max_length=250,null=True, blank=True)
    description = models.CharField(max_length=1000,null=True, blank=True)
    author = models.CharField(max_length=100,null=True, blank=True)
    date_from = models.DateField()
    video_length= models.CharField(max_length=20,null=True, blank=True)
    movie_check = models.BooleanField(default=False)
    short_movie_check = models.BooleanField(default=False)
    nature_check = models.BooleanField(default=False)
    funny_check = models.BooleanField(default=False)
    knowledge_check = models.BooleanField(default=False)
    other_check = models.BooleanField(default=False)
    age_rating = models.PositiveIntegerField(default=0)
    upload_visible_check = models.BooleanField(default=False)


