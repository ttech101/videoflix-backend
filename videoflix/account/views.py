from base64 import urlsafe_b64encode
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User




# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [] #permissions.IsAuthenticated


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            # 'user_id': user.pk,
            'name' : user.first_name + ' ' + user.last_name,
            # 'email': user.email,
        })

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            try:
                # email.send()
                return JsonResponse({'ok': "You have successfully registered. Please check your email!"})
            except Exception as e:
                return HttpResponse(f"Error sending email: {str(e)}")
        else:

            email = form.cleaned_data['email']
            print(email)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': {'email': 'This email is already registered.'}})
            else:
                errors = {
                    'email': form.errors.get('email', None),
                    'password1': form.errors.get('password1', None),
                    'password2': form.errors.get('password2', None),
                }
                return JsonResponse({'error': errors})
    else:
        form = CustomUserCreationForm()
    return HttpResponseBadRequest("Invalid request method")