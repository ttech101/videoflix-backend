from django.conf import settings
from django.http import  HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets ,status
from rest_framework.parsers import MultiPartParser
from storage.models import uploadMovie
from storage.serializers import PreviewSerializer
from .models import UserProfile
from .serializers import UserProfileSerializer
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
from django.shortcuts import  render,render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.utils.crypto import get_random_string
from .models import  PasswordResetToken
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model



# Create your views here.
@permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user profiles.
    This ViewSet provides CRUD operations for user profiles.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class LoginView(ObtainAuthToken):
    """
    Custom view for user login.
    This view handles user authentication and provides a token on successful login.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST request for user login.
        Parameters:
        - request: Request object.
        Returns:
        - Response: JSON response containing session key, authentication token, user name, avatar path, autoplay status, and language.
        """
        if request.method == 'POST':
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
            return Response({
                'session': request.session.session_key,
                'token': token.key,
                'name' : user.first_name + ' ' + user.last_name,
                'avatar_path': avatar_path,
                'autoplay': user_profile.automatic_playback,
                'language': user_profile.language
            })


    def get(self, request, *args, **kwargs):
        """
        Check if a user exists.
        Returns:
        - Response: JSON response indicating whether the user exists or not.
        """
        if request.method == 'GET':
            if request.user.is_authenticated:
                return Response({'user_exists': True})
            email = request.query_params.get('email', None)
            if email:
                user_exists = User.objects.filter(email=email).exists()
                return Response({'user_exists': user_exists})
            else:
                return Response({'detail': 'Email parameter missing'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def register(request):
    """
    View for user registration.
    This view handles user registration via POST request.
    """
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
    """
    View for activating user account.
    This view handles the activation of user account using the activation link.
    """
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
    """
    View for checking token validity.
    This view checks if the provided token exists in the database.
    """
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
    """
    View for resetting user password.
    This view handles the process of resetting user password and sending a reset email.
    """
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
    """
    View for changing user password using a reset token.
    This view handles the process of changing user password using a reset token.
    """
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
    """
    View for deleting the current user account.
    This view handles the process of deleting the current user account.
    """
    user = request.user
    try:
        email = createMailDeleteAccount(request,user)
        email.send()
        user.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


class UserProfileView(APIView):
    """
    View for managing user profiles.
    This view provides endpoints for retrieving, updating, and uploading user profile information.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    def get(self, request, *args, **kwargs):
        """
        Get user profile information.
        Returns:
        - JsonResponse: JSON response containing user profile information.
        """
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
        """
        Update user profile.
        Returns:
        - Response: HTTP response indicating success.
        """
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
        """
        Upload avatar for user profile.
        Returns:
        - Response: HTTP response indicating success or failure.
        """
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
    """
    View for changing user email and username.
    This view handles the process of changing user email and username.
    """
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
    """
    View for managing user watchlist.
    This view provides endpoints for adding, retrieving, and removing movies from the user's watchlist.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        """
        Add a movie to the user's watchlist.
        Returns:
        - Response: JSON response indicating success or failure.
        """
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
        """
        Retrieve movies from the user's watchlist.
        Returns:
        - Response: JSON response containing movie data.
        """
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
        """
        Remove a movie from the user's watchlist.
        Returns:
        - Response: JSON response indicating success or failure.
        """
        key_to_delete = request.data.get('key', None)
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