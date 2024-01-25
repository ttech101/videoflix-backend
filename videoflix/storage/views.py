from django.shortcuts import render
from storage.models import uploadMovie
from storage.serializers import MovieSerializer,PreviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import viewsets ,status


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