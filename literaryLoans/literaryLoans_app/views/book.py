from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from ..models import Book, User, Genre
from ..serializers import BookSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
import json


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class=BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset()
        print("queryset", queryset)
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)
    

class BookDestroyAPIView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    lookup_field='id'


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createBook(request):
    if request.method == 'POST':
        try:
            user = request.user
            data = request.body
            json_data = json.loads(data.decode('utf-8'))
            # Retrieve the lender user instance
            lender = user
            print(lender)
            print("body",json_data)
            data = json_data['bookDetails']
            title_book = data['bookName']
            print("title",title_book)
            genre_id = data['bookGenre']
            bookgenre = Genre.objects.get(id = genre_id)
            # Create a new book instance and set the lender_id field
            new_book = Book.objects.create(
                title = data['bookName'],
                description = data['bookDescription'],
                lender_id = lender,
                price = data['price'],
                image = data['coverImageUrl'],
                author = data['authorName'],
                quantity = data['quantity'],
                genre = bookgenre
            )
            print("new book", new_book)
            new_book.save()

            return JsonResponse({"message": "success"})
        except User.DoesNotExist:
            return JsonResponse({"error": "Lender does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
