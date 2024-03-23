from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models import Genre, Book
from ..serializers import GenreSerializer, BookSerializer
from rest_framework.response import Response

class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class=GenreSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset()
        print("queryset", queryset)
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data)

class BooksByGenreAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        genre = self.kwargs['genre_id']
        genre_id = Genre.objects.get(title = genre)
        return Book.objects.filter(genre_id=genre_id)
    