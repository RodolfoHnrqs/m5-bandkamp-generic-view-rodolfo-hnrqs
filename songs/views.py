from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Song
from rest_framework.pagination import PageNumberPagination
from .serializers import SongSerializer
from albums.models import Album
from rest_framework import generics

class ExtensionPagination(PageNumberPagination):
    page_size=1

class SongView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    lookup_url_kwarg="pk"

    pagination_class = ExtensionPagination

    def perform_create(self, serializer):
        find_album = get_object_or_404(Album, id=self.kwargs.get("pk"))
        serializer.save(album=find_album)