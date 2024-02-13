import uuid
from django.forms import ValidationError
from django.http import HttpResponseBadRequest, JsonResponse
from storage.models import uploadMovie
from storage.serializers import MovieSerializer,PreviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import viewsets ,status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.utils.translation import gettext_lazy as _


@permission_classes([IsAuthenticated])
class MovieView(viewsets.ModelViewSet):
    """
    ViewSet for managing movie uploads.
    This ViewSet provides endpoints for listing, creating, updating, and deleting movie uploads.
    """
    queryset = uploadMovie.objects.filter(upload_visible_check=True)
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get_queryset(self):
        select = self.request.query_params.get('select', None)
        return uploadMovie.objects.filter(random_key=select)

@permission_classes([IsAuthenticated])
class CheckWatchlist(viewsets.ModelViewSet):
    """
    ViewSet for checking if a movie is in the user's watchlist.
    This ViewSet provides an endpoint for checking if a movie is in the user's watchlist.
    """
    queryset = uploadMovie.objects.filter(upload_visible_check=True)
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def list(self, request, *args, **kwargs):
        """
        Check if a movie is in the user's watchlist.
        Parameters:
        - request: Request object.
        Returns:
        - Response: Boolean indicating whether the movie is in the user's watchlist.
        """
        select = request.query_params.get('select', None)
        user_profile = request.user.userprofile
        watchlist = user_profile.watchlist if user_profile.watchlist else []
        if select in watchlist:
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response(False, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class PreviewSerializer(viewsets.ModelViewSet):
    """
    ViewSet for previewing movies.
    This ViewSet provides endpoints for previewing movies.
    """
    queryset = uploadMovie.objects.filter(upload_visible_check=True)
    serializer_class = PreviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        age_rating_user = user.userprofile.age_rating
        select = self.request.query_params.get('select', None)

        filter_params = {
            'upload_visible_check': True,
            'age_rating__lte': age_rating_user,
            'convert_status': 2
        }
        if select == 'newHeader':
            return uploadMovie.objects.filter(**filter_params).order_by('-created_at')[:3]
        elif select == 'new':
            return uploadMovie.objects.filter(**filter_params).order_by('-created_at')[:20]
        elif select in ['other', 'nature', 'funny', 'knowledge', 'movie']:
            filter_params[f'{select}_check'] = True
            return uploadMovie.objects.filter(**filter_params)[:20]
        elif select == 'serie':
            filter_params['short_movie_check'] = True
            return uploadMovie.objects.filter(**filter_params)[:20]
        elif select == 'my':
            return uploadMovie.objects.filter(user=self.request.user, convert_status__gte=1)[:50]
        elif select == 'my-uploads':
            return uploadMovie.objects.filter(user=self.request.user, convert_status__gte=1)
        elif select == 'all':
            return uploadMovie.objects.filter(**filter_params)[:20]
        else:
            return []


class CreateMovie(APIView):
    """
    API View for creating a movie upload.
    This API View provides endpoints for creating a new movie upload and updating movie details.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        """
        Create a new movie upload.
        Parameters:
        - request: Request object.
        Returns:
        - JsonResponse: JSON response with a random key for the created movie.
        """
        movie = uploadMovie.objects.create(user=request.user)
        movie.save()
        response_data = {'random_key': str(movie.random_key)}
        return JsonResponse(response_data)

    def post(self, request, *args, **kwargs):
        """
        Update movie details based on POST request data.
        Parameters:
        - request: Request object.
        Returns:
        - JsonResponse: JSON response indicating success or error.
        """
        try:
            random_key = request.data.get('upload_key')
            if not random_key:
                return JsonResponse({'error': 'Missing "random_key" in the request data'}, status=400)
            movie = uploadMovie.objects.get(random_key=random_key)
            self.update_movie_from_request_data(movie, request.data)
            return JsonResponse({'success': 'Movie details successfully updated'})
        except uploadMovie.DoesNotExist:
            return JsonResponse({'error': 'Invalid "random_key"'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request, *args, **kwargs):
        """
        Update movie details based on PUT request data.
        Parameters:
        - request: Request object.
        Returns:
        - JsonResponse: JSON response indicating success or error.
        """
        try:
            random_key = request.data.get('upload_key')
            if not random_key:
                return JsonResponse({'error': 'Missing "random_key" in the request data'}, status=400)
            movie = uploadMovie.objects.get(random_key=random_key)
            self.update_movie_from_request_data(movie, request.data)
            return JsonResponse({'success': 'Movie details successfully updated'})
        except uploadMovie.DoesNotExist:
            return JsonResponse({'error': 'Invalid "random_key"'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def update_movie_from_request_data(self, movie, data):
        """
        Update movie object with data from request.
        Parameters:
        - movie: Movie object to be updated.
        - data: Data from the request.
        """
        movie.author = data.get('author', '')
        movie.description = data.get('description', '')
        movie.description_short = data.get('description_short', '')
        movie.genre = data.get('genre', '')
        movie.movie_check = data.get('movie_check', False)
        movie.date_from = data.get('date_from', '')
        movie.short_movie_check = data.get('short_movie_check', False)
        movie.nature_check = data.get('nature_check', False)
        movie.funny_check = data.get('funny_check', False)
        movie.knowledge_check = data.get('knowledge_check', False)
        movie.other_check = data.get('other_check', False)
        movie.movie_name = data.get('movie_name', '')
        movie.age_rating = data.get('selectedAge', 0)
        movie.upload_visible_check = data.get('upload_visible_check', False)
        movie.video_length = data.get('video_length', '')
        movie.automatic_cover = data.get('automatic_cover', True)
        movie.automatic_image = data.get('automatic_image', True)
        movie.save()


class UploadMovie(APIView):
    """
    API View for uploading a movie file.
    This API View provides endpoints for uploading a movie file.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    MAX_COVER_SIZE_MB = 2
    MAX_BIG_PICTURE_SIZE_MB = 5
    MAX_VIDEO_SIZE_MB = 150
    def validate_file_size(self, file, max_size_mb, field_name):
        """
        Validate file size.
        Parameters:
        - file: File object.
        - max_size_mb: Maximum size allowed in megabytes.
        - field_name: Name of the field (e.g., 'Cover', 'Big Picture', 'Video').
        Raises:
        - ValidationError: If the file size exceeds the maximum allowed size.
        """
        if file:
            max_size_bytes = max_size_mb * 1024 * 1024
            if file.size > max_size_bytes:
                raise ValidationError(_(f"The size of the {field_name} with the file name {file} has been exceeded, the maximum permitted size is {max_size_mb} MB."))
    def get_random_key_uuid(self, random_key):
        """
        Get UUID from random key.
        Parameters:
        - random_key: Random key as string.
        Returns:
        - UUID: UUID object parsed from the random key.
        Raises:
        - HttpResponseBadRequest: If the provided random key is invalid.
        """
        try:
            return uuid.UUID(random_key)
        except ValueError:
            raise HttpResponseBadRequest("Invalid 'upload_key'. Please provide a valid UUID.")
    def get_movie_by_random_key(self, random_key_uuid):
        """
        Get movie object by random key.
        Parameters:
        - random_key_uuid: Random key as UUID object.
        Returns:
        - uploadMovie: Movie object with the provided random key.
        Raises:
        - HttpResponseBadRequest: If no movie is found with the provided random key.
        """
        try:
            return uploadMovie.objects.get(random_key=random_key_uuid)
        except uploadMovie.DoesNotExist:
            raise HttpResponseBadRequest("No movie found with the provided 'upload_key'.")
    def post(self, request, *args, **kwargs):
        """
        Handle POST request for uploading movie files.
        Parameters:
        - request: Request object.
        Returns:
        - Response: JSON response indicating success or error.
        """
        try:
            random_key = request.POST.get('upload_key')
            cover_file = request.FILES.get('cover')
            image_file = request.FILES.get('image')
            video_file = request.FILES.get('video')
            random_key_uuid = self.get_random_key_uuid(random_key)
            movie = self.get_movie_by_random_key(random_key_uuid)
            self.validate_file_size(cover_file, self.MAX_COVER_SIZE_MB, "Cover")
            self.validate_file_size(image_file, self.MAX_BIG_PICTURE_SIZE_MB, "Big Picture")
            self.validate_file_size(video_file, self.MAX_VIDEO_SIZE_MB, "Video")
            if cover_file:
                movie.cover = cover_file
            if image_file:
                movie.big_picture = image_file
            if video_file:
                movie.video = video_file
            movie.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return HttpResponseBadRequest(str(e))
        except Exception as e:
            return HttpResponseBadRequest(str(e))

class DeleteMovie(APIView):
    """
    API View for deleting a movie.
    This API View provides an endpoint for deleting a movie.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def delete(self, request, *args, **kwargs):
        """
        Delete a movie.
        Parameters:
        - request: Request object.
        Returns:
        - JsonResponse: JSON response indicating success or error.
        """
        try:
            random_key = request.data.get('random_key')
            if not random_key:
                return JsonResponse({'error': 'Missing "random_key" in the request data'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                movie = uploadMovie.objects.get(random_key=random_key)
            except uploadMovie.DoesNotExist:
                return JsonResponse({'error': 'No movie found with the provided "random_key"'}, status=status.HTTP_404_NOT_FOUND)
            movie.delete()
            return JsonResponse({'success': 'Movie successfully deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)