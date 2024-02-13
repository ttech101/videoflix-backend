import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class uploadMovie(models.Model):
    """
    Model representing uploaded movies.
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
        """
        if not self.pk:
            self.random_key = uuid.uuid4()
        super().save(*args, **kwargs)


