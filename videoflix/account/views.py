from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import authentication
from .models import UserProfile,UserModel
from .serializers import UserProfileSerializer, UserModelSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import  force_str
from django.contrib.auth.models import User
from .functions import check_token_in_database, createMailActivateAccount
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.utils.crypto import get_random_string
from .models import  PasswordResetToken
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404





# Create your views here.

@permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


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
            email = createMailActivateAccount(request,user)
            try:
                email.send()
                return JsonResponse({'ok': "You have successfully registered. Please check your email!"})
            except Exception as e:
                return HttpResponse(f"Error sending email: {str(e)}")
        else:
            email = form.cleaned_data['email']
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

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        url = settings.FRONTEND_URL
        return render(request, 'activation_complete.html', {'url': url})
    else:
        return render(request, 'activation_failed.html')


def check_token(request):
    token = request.GET.get('token')
    if token:
        token_exists = check_token_in_database(token)
        if token_exists:
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False})
    else:
        return JsonResponse({'status': 'Token nicht übermittelt'})

@api_view(['POST',])
@permission_classes([AllowAny])
def reset_password(request):

    if request.method == 'POST':
        email = request.data.get('email')
        print(email)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'This email address does not exist in the system.'})
        token = get_random_string(length=32)
        password_reset_token, created = PasswordResetToken.objects.get_or_create(user=user)
        password_reset_token.reset_password_token = token
        password_reset_token.save()
        reset_link = f"{settings.FRONTEND_URL}/landing-reset-password?password-reset&token={token}"
        subject = 'Reset password'
        message = render_to_string('password_reset_email.html', {'user': user,'reset_link': reset_link})
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, html_message=message)
        return JsonResponse({'success': 'We have sent you an email to reset'})
    else:
        return JsonResponse({'error': 'invalid request'}, status=400)

@api_view(['POST',])
@permission_classes([AllowAny])
def change_password(request):
    if request.method == 'POST':
        token = request.data.get('token')
        password = request.data.get('password')
        token_obj = get_object_or_404(PasswordResetToken, reset_password_token=token)
        user = token_obj.user
        user.set_password(password)
        user.save()
        token_obj.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Ungültige Anfrage'}, status=400)


@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_current_user(request):
    user = request.user
    try:
        user.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# class UserProfileView(View):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = []
#     print('hallo')
#     def get(self, request, *args, **kwargs):
#         user_profile = UserProfile.objects.get(user=request.user)

#         data = {
#             'avatar': user_profile.avatar.url if user_profile.avatar else None,
#             'automatic_playback': user_profile.automatic_playback,
#             'language': user_profile.language,
#             'age_rating': user_profile.age_rating,
#         }

#         return JsonResponse(data)

class UserProfileView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
          # Filtere das UserProfile-Objekt des authentifizierten Benutzers
          user_profile = UserProfile.objects.filter(user=request.user).first()
          user = UserModel.objects.filter(user=request.user).first()
          # Überprüfe, ob das UserProfile-Objekt existiert
          if user_profile:
              serializer = UserProfileSerializer(user_profile)
              serializer_user = UserModelSerializer(user)
              print(serializer_user.data)

              return Response(serializer.data)
          else:
              # Benutzer hat kein UserProfile
              return Response({'detail': 'UserProfile not found for this user.'})