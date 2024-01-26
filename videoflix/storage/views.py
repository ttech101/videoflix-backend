import json
import uuid
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from storage.models import uploadMovie
from storage.serializers import MovieSerializer,PreviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import viewsets ,status
from rest_framework.decorators import permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView


@permission_classes([IsAuthenticated])
class MovieView(viewsets.ModelViewSet):
    queryset = uploadMovie.objects.filter(upload_visible_check=True)
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        select = self.request.query_params.get('select', None)
        return uploadMovie.objects.filter(random_key=select)




@permission_classes([IsAuthenticated])
class PreviewSerializer(viewsets.ModelViewSet):
    queryset = uploadMovie.objects.filter(upload_visible_check=True)
    serializer_class = PreviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get_queryset(self):
        select = self.request.query_params.get('select', None)
        if select == 'newHeader':
            return uploadMovie.objects.filter( upload_visible_check=True).order_by('-created_at')[:3]
        if select == 'new':
            return uploadMovie.objects.filter( upload_visible_check=True).order_by('-created_at')
        if select == 'other':
            return uploadMovie.objects.filter(other_check=True, upload_visible_check=True)
        if select == 'nature':
            return uploadMovie.objects.filter(nature_check=True, upload_visible_check=True)
        if select == 'funny':
            return uploadMovie.objects.filter(funny_check=True, upload_visible_check=True)
        if select == 'knowledge':
            return uploadMovie.objects.filter(knowledge_check=True, upload_visible_check=True)
        if select == 'movie':
            return uploadMovie.objects.filter(movie_check=True, upload_visible_check=True)
        if select == 'serie':
            return uploadMovie.objects.filter(short_movie_check=True, upload_visible_check=True)
        if select == 'my':
            return uploadMovie.objects.filter(user=self.request.user)
        if select == 'all':
            return uploadMovie.objects.filter(upload_visible_check=True)



class CreateMovie(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, *args, **kwargs):
        # Hier wird ein neues uploadMovie-Objekt erstellt
        movie = uploadMovie.objects.create(user=request.user)
        print(movie)
        movie.save()
        response_data = {'random_key': str(movie.random_key)}
        return JsonResponse(response_data)

    def post(self, request, *args, **kwargs):
        try:
            random_key = request.data.get('upload_key')
            if not random_key:
                return JsonResponse({'error': 'Missing "random_key" in the request data'}, status=400)
            movie = uploadMovie.objects.get(random_key=random_key)
            movie.author = request.data.get('author', '')
            movie.description = request.data.get('description', '')
            movie.description_short = request.data.get('description_short', '')
            movie.genre = request.data.get('genre', '')
            movie.movie_check = request.data.get('movie_check', False)
            movie.short_movie_check = request.data.get('short_movie_check', False)
            movie.nature_check = request.data.get('nature_check', False)
            movie.funny_check = request.data.get('funny_check', False)
            movie.knowledge_check = request.data.get('knowledge_check', False)
            movie.other_check = request.data.get('other_check', False)
            movie.movie_name = request.data.get('movie_name', '')
            movie.age_rating = request.data.get('selectedAge', 0)
            movie.upload_visible_check = request.data.get('upload_visible_check', False)
            movie.video_length = request.data.get('video_length', '')
            movie.save()
            return JsonResponse({'success': 'Movie details successfully updated'})
        except uploadMovie.DoesNotExist:
            return JsonResponse({'error': 'Invalid "random_key"'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class UploadMovie(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        try:
            random_key = request.POST.get('upload_key')
            cover_file = request.FILES.get('cover')
            image_file = request.FILES.get('image')
            video_file = request.FILES.get('video')
            try:
                random_key_uuid = uuid.UUID(random_key)
            except ValueError:
                return HttpResponseBadRequest("Invalid 'upload_key'. Please provide a valid UUID.")
            try:
                movie = uploadMovie.objects.get(random_key=random_key_uuid)
            except uploadMovie.DoesNotExist:
                return HttpResponseBadRequest("No movie found with the provided 'upload_key'.")
            if cover_file:
                movie.cover = cover_file
            if image_file:
                movie.big_picture = image_file
            if video_file:
                movie.video = video_file
            movie.save()
            return Response({"status":"success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponseBadRequest(str(e))