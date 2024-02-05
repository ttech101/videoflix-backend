from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
import os


# Create confirmation email
def createMailActivateAccount(request,user):
    current_site = get_current_site(request)
    subject = 'Activate your account for Videofilx'
    message = render_to_string('registration_confirmation_email.html', {
        'user': user,
        'confirmation_link': f"http://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}",
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = 'html'
    return email

def createMailNewAccount(request,user):
    subject = 'New user for Videoflix'
    message = render_to_string('new_user.html', {
        'user': user,
    })
    email = EmailMessage(subject, message, to=['admin@tech-mail.eu'])
    email.content_subtype = 'html'
    return email


def createMailDeleteAccount(request,user):
    subject = 'Deletet Account from Videoflix'
    message = render_to_string('delete_acc.html', {
        'user': user,
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = 'html'
    return email

def check_token_in_database(token):
    try:
        token_obj = Token.objects.get(key=token)
        return True  # Token gefunden
    except Token.DoesNotExist:
        return False  # Token nicht gefunden

def handle_uploaded_avatar(user_profile, avatar_file):
    allowed_extensions = ['.png', '.jpg']
    max_file_size = 2 * 1024 * 1024  # 2 MB
    _, file_extension = os.path.splitext(avatar_file.name)
    if (file_extension.lower() in allowed_extensions) and (avatar_file.size <= max_file_size):
        if user_profile.avatar:
            old_avatar_path = user_profile.avatar.path
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)
        user_profile.avatar = avatar_file
        user_profile.save()
        return {'message': 'Image uploaded successfully', 'status': status.HTTP_200_OK}
    else:
        return {'message': 'Only .png and .jpg files up to 2 MB are allowed', 'status': status.HTTP_400_BAD_REQUEST}