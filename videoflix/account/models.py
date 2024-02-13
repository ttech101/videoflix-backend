from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class UserModel(models.Model):
    """
    Model representing additional user data.
    Attributes:
    """
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True)

class UserProfile(models.Model):
    """
    Model representing user profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    created_at = models.DateField(default=datetime.today)
    last_logged_in = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    automatic_playback = models.BooleanField(default=False)
    language = models.CharField(max_length=50, default='en')
    age_rating = models.PositiveIntegerField(default=0)
    watchlist = models.JSONField(blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a user profile when a new user is created.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal receiver function to save user profile when the associated user is saved.
    """
    instance.userprofile.save()

class PasswordResetToken(models.Model):
    """
    Model representing password reset tokens.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)