from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class UserModel(models.Model):
    """
    Model representing additional user data.
    Attributes:
        username (User): The associated user object.
        first_name (str): The first name of the user.
        email (str): The email address of the user.
    """
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True)

class UserProfile(models.Model):
    """
    Model representing user profile information.
    Attributes:
        user (User): The associated user object.
        created_at (DateTime): The date and time when the profile was created.
        last_logged_in (DateTime): The date and time of the last login.
        avatar (ImageField): The user's profile picture.
        automatic_playback (bool): Flag indicating automatic playback preference.
        language (str): The preferred language for the user.
        age_rating (int): The preferred age rating for content.
        watchlist (JSONField): JSON data representing the user's watchlist.
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
    Args:
        sender: The sender of the signal.
        instance (User): The user instance.
        created (bool): Indicates if the user was created or updated.
        kwargs: Additional keyword arguments.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal receiver function to save user profile when the associated user is saved.
    Args:
        sender: The sender of the signal.
        instance (User): The user instance.
        kwargs: Additional keyword arguments.
    """
    instance.userprofile.save()

class PasswordResetToken(models.Model):
    """
    Model representing password reset tokens.
    Attributes:
        user (User): The associated user object.
        reset_password_token (str): The password reset token.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)