from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from literaryLoans_app.models import Rented, ReturnRequest, Book
from literaryLoans_app.serializers import BookSerializerReturn, ReturnRequestSerializer
from rest_framework import generics
import datetime

class ReturnRequestListAPIView(generics.ListAPIView):
    serializer_class=ReturnRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        queryset = ReturnRequest.objects.filter(lender=user.id).filter(status='0').order_by('request_date')
        serializer = ReturnRequestSerializer(queryset, many=True)
        return Response(serializer.data) 

from rest_framework import serializers

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_return_request(request):
    if request.method == 'POST':
        json_data = request.data['bookDetails']
        rented_id = json_data['rented_id']
        try:
            rented_instance = Rented.objects.get(id=rented_id)
        except Rented.DoesNotExist:
            return Response({"error": "Rented instance with the provided ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if a ReturnRequest already exists for this Rented instance
        existing_return_request = ReturnRequest.objects.filter(rented_id=rented_instance.id).exists()
        if existing_return_request:
            return Response({"error": "ReturnRequest already exists for this Rented instance"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new instance of ReturnRequest with the existing Book instance
        new_return_request_instance = ReturnRequest.objects.create(
            borrower=rented_instance.borrower,
            lender=rented_instance.lender,
            book=rented_instance.book,
            quantity=rented_instance.quantity,
            rented_id=rented_instance
        )

        # Optionally, set the request_date field
        new_return_request_instance.request_date = datetime.date.today()
        new_return_request_instance.save()

        # Serialize the created ReturnRequest instance
        serializer = ReturnRequestSerializer(new_return_request_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def accept_return_request(request):
    if request.method == 'POST':
        json_data = request.data['bookDetails']
        return_request_id = json_data['request_id']
        try:
            return_request_instance = ReturnRequest.objects.get(id=return_request_id)
        except ReturnRequest.DoesNotExist:
            return Response({"error": "ReturnRequest instance with the provided ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        # Update status to 'Accepted'
        return_request_instance.status = '1'  # Assuming '1' represents 'Accepted' status
        return_request_instance.save()
        rented = return_request_instance.rented_id
        book = return_request_instance.book
        book_instance = Book.objects.get(id = book.id)
        book_instance.quantity += return_request_instance.quantity
        book_instance.available = True
        book_instance.save()

        try:
            rented_instance = Rented.objects.get(id=rented.id)
        except Rented.DoesNotExist:
            return Response({"error": "Rented instance with the provided ID does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Delete rented_instance
        rented_instance.delete()
        return Response({"message": "Return request accepted successfully"}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def lender_return(request):
    if request.method == 'POST':
        json_data = request.data
        rented_id = json_data['rented_id']
        try:
            rented_instance = Rented.objects.get(id=rented_id)
        except Rented.DoesNotExist:
            return Response({"error": "Rented instance with the provided ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        # Update quantity and available status of the corresponding book
        book_instance = rented_instance.book
        book_instance.quantity += rented_instance.quantity
        book_instance.available = True
        book_instance.save()

        # Delete the rented instance
        rented_instance.delete()

        return Response({"message": "Return by lender processed successfully"}, status=status.HTTP_200_OK)
