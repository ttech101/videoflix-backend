import os
from django.conf import settings
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets ,status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from storage.models import uploadMovie
from storage.serializers import PreviewSerializer
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
from .functions import check_token_in_database, createMailActivateAccount, createMailDeleteAccount, createMailNewAccount, handle_uploaded_avatar
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
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login


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
        try:
            user_profile = user.userprofile
            avatar_path = user_profile.avatar.url if user_profile.avatar else None
        except UserProfile.DoesNotExist:
            avatar_path = None
        my_view(request)
        return Response({
            'session': request.session.session_key,
            'token': token.key,
            # 'user_id': user.pk,
            'name' : user.first_name + ' ' + user.last_name,
            'avatar_path': avatar_path,
            'autoplay': user_profile.automatic_playback,
            'language': user_profile.language
        })


    def get(self, request, *args, **kwargs):
        # Überprüfen, ob der Benutzer angemeldet ist
        if request.user.is_authenticated:
            return Response({'user_exists': True})
        # Wenn der Benutzer nicht authentifiziert ist, überprüfen Sie die E-Mail-Adresse
        email = request.query_params.get('email', None)
        if email:
            user_exists = User.objects.filter(email=email).exists()
            return Response({'user_exists': user_exists})
        else:
            return Response({'detail': 'Email parameter missing'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def my_view(request):
    print('???')
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        print('login faild')
        # Return an 'invalid login' error message.
        ...


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email = createMailActivateAccount(request,user)
            emai_new_user = createMailNewAccount(request,user)
            try:
                email.send()
                emai_new_user.send()
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
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'This email address does not exist in the system.'}, status=400)
        token = get_random_string(length=32)
        password_reset_token, created = PasswordResetToken.objects.get_or_create(user=user)
        password_reset_token.reset_password_token = token
        password_reset_token.save()
        reset_link = f"{settings.FRONTEND_URL}/landing-reset-password?password-reset&token={token}"
        subject = 'Reset password'
        message = render_to_string('password_reset_email.html', {'user': user, 'reset_link': reset_link})
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
        email = createMailDeleteAccount(request,user)
        email.send()
        user.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        user = request.user
        data = {
            'avatar': user_profile.avatar.url if user_profile.avatar else None,
            'automatic_playback': user_profile.automatic_playback,
            'language': user_profile.language,
            'age_rating': user_profile.age_rating,
            'name': user.first_name,
        }
        return JsonResponse(data)
    def put(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        user = request.user
        user_profile.automatic_playback = request.data.get('automatic_playback', user_profile.automatic_playback)
        user_profile.language = request.data.get('language', user_profile.language)
        user_profile.age_rating = request.data.get('age_rating', user_profile.age_rating)
        user_profile.save()
        user.first_name = request.data.get('name', user.first_name)
        user.save()
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        avatar_file = request.FILES.get('avatar')

        if avatar_file:
            response = handle_uploaded_avatar(user_profile, avatar_file)
            return Response(response, status=response['status'])
        else:
            return Response({'message': 'No file found in the request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@authentication_classes([TokenAuthentication])
def change_email_and_username(request):
    user = request.user
    if request.method == 'GET':
        return Response({'email': user.email})
    new_email = request.data.get('new_email')
    new_username = request.data.get('new_username')
    if not new_email or not new_username:
        return Response({'error': 'Both new email and new username are required.'}, status=400)
    if get_user_model().objects.filter(email=new_email).exclude(pk=user.pk).exists():
        return Response({'error': 'Email already exists.'}, status=400)
    if get_user_model().objects.filter(username=new_username).exclude(pk=user.pk).exists():
        return Response({'error': 'Username already exists.'}, status=400)
    user.email = new_email
    user.username = new_username
    user.save()
    return Response({'success': 'Email changed successfully.'})

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
def change_password_acc(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    if not current_password or not new_password:
        return Response({'error': 'Both current_password and new_password are required.'}, status=400)
    if not user.check_password(current_password):
        return Response({'error': 'Current password is incorrect.'}, status=400)
    user.set_password(new_password)
    user.save()

    return Response({'success': 'Password changed successfully.'})


class Watchlist(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        key_to_add = request.data.get('key', None)
        if key_to_add:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)
            watchlist = user_profile.watchlist or []
            if key_to_add not in watchlist:
                watchlist.append(key_to_add)
                user_profile.watchlist = watchlist
                user_profile.save()
                return Response({'success': 'Key added to watchlist'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Key already exists in watchlist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Key not provided in the POST data'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)
        watchlist = user_profile.watchlist or []
        preview_data = []
        for key in watchlist:
            try:
                movie_instance = uploadMovie.objects.get(random_key=key)
                serializer = PreviewSerializer(movie_instance, context={'request': request})
                preview_data.append(serializer.data)
            except uploadMovie.DoesNotExist:
                # Handhaben Sie den Fall, wenn das Movie-Objekt nicht gefunden wurde
                pass
        return Response(preview_data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        key_to_delete = request.data.get('key', None)
        print(key_to_delete)
        if key_to_delete:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)
            watchlist = user_profile.watchlist or []
            if key_to_delete in watchlist:
                watchlist.remove(key_to_delete)
                user_profile.watchlist = watchlist
                user_profile.save()
                return Response({'success': 'Key removed from watchlist'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Key not found in watchlist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Key not provided in the DELETE data'}, status=status.HTTP_400_BAD_REQUEST)


def serve_protected_media(request, path):
    """
    Diese View dient zum Schutz des direkten Zugriffs auf Dateien im Media-Ordner.
    Sie prüft, ob der Benutzer authentifiziert ist und die erforderlichen Berechtigungen hat.
    """
    # Bilden Sie den vollständigen Pfad zur angeforderten Datei im Media-Ordner.
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    # Überprüfen Sie, ob die angeforderte Datei tatsächlich im Media-Ordner liegt.
    if os.path.exists(file_path):
        # Überprüfen Sie, ob der Benutzer authentifiziert ist und die Berechtigungen hat.
        if request.user.is_authenticated and request.user.has_perm('storage.can_access_media'):
            # Bedienen Sie die Datei, wenn der Benutzer authentifiziert und autorisiert ist.
            return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
        else:
            # Wenn der Benutzer nicht authentifiziert ist oder die Berechtigungen fehlen,
            # geben Sie einen 403-Fehler zurück.
            return HttpResponseForbidden('Zugriff verweigert.')
    else:
        # Wenn die Datei nicht existiert, geben Sie einen 404-Fehler zurück.
        return HttpResponseNotFound('Datei nicht gefunden.')


def get_sessionid(request):
    sessionid = request.session.session_key
    if sessionid:
        return JsonResponse({'sessionid': sessionid})
    else:
        return JsonResponse({'error': 'Sessionid not found'}, status=400)