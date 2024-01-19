from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


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

def check_token_in_database(token):
    try:
        token_obj = Token.objects.get(key=token)
        return True  # Token gefunden
    except Token.DoesNotExist:
        return False  # Token nicht gefunden