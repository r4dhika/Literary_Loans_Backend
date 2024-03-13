from rest_framework import generics
from ..models import Book
from ..serializers import BookSerializer

class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class=BookSerializer


class BookDestroyAPIView(generics.DestroyAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    lookup_field='book_id'