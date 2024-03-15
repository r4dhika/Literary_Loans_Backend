from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from ..models import Book, User
from ..serializers import BookSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
import json


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class=BookSerializer

class BookDestroyAPIView(generics.DestroyAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    lookup_field='book_id'

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createBook(request):
    if request.method == 'POST':
        try:
            email = request.user
            data = request.body
            json_data = json.loads(data.decode('utf-8'))
            # Retrieve the lender user instance
            lender = User.objects.get(email=email)
            print(lender)

            # Create a new book instance and set the lender_id field
            new_book = Book.objects.create(
                title=json_data.get('title', ''),
                description=json_data.get('description', ''),
                lender_id=lender,
                price=json_data.get('price', 0.00),
                penalty=json_data.get('penalty', 0.00),
                quantity=json_data.get('quantity', 0),
                image=json_data.get('image', '')
            )
            new_book.save()

            return JsonResponse({"message": "success"})
        except User.DoesNotExist:
            return JsonResponse({"error": "Lender does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
