from rest_framework import generics
from ..models import BorrowRequest,User,Book,Rented
from ..serializers import BorrowRequestSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
import json
import datetime
from rest_framework.response import Response

class BorrowRequestListAPIView(generics.ListAPIView):
    serializer_class=BorrowRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        queryset = BorrowRequest.objects.filter(lender=user.id).filter(status='0').order_by('request_date')
        serializer = BorrowRequestSerializer(queryset, many=True)
        return Response(serializer.data)    
    
class BorrowRequestStatusListAPIView(generics.ListAPIView):
    serializer_class=BorrowRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        queryset = BorrowRequest.objects.filter(borrower=user.id).filter(status="0").order_by('-request_date')
        serializer = BorrowRequestSerializer(queryset, many=True)
        data = serializer.data  # Extract data from the serializer
        for item in data:
            if item['status'] == "1":
                item['status'] = "Accepted"
            elif item['status'] == "2":
                item['status'] = "Cancelled"
            else:
                item['status'] = "Pending"
        return Response(serializer.data)   

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createBorrowRequest(request):
    if request.method == 'POST':
        try:
            data=request.body
            json_data = request.data['bookDetails']
            book_id=json_data['book_id']
            book=Book.objects.get(id=book_id)
            lender_id=book.lender_id
            lender=User.objects.get(email=lender_id)
            borrower=request.user
            print("book quantitiy", book.quantity)
            print("requested quantity", json_data['quantity'])
            if (book.quantity < json_data['quantity']):
                return JsonResponse({"error": "Requested quantity exceeds available quantity"}, status=400)

            new_borrowrequest = BorrowRequest.objects.create(
                borrower=borrower,
                lender=lender,
                book=book,
                status='0',
                quantity=json_data['quantity'],
                request_date=datetime.date.today(),  
                return_date=json_data['return_date']
            )
            new_borrowrequest.save()

            return JsonResponse({"message": "success"})
        except User.DoesNotExist:
            return JsonResponse({"error": "Lender does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def acceptBorrowRequest(request):
    if request.method == 'POST':
        try:
            json_data = request.data['bookDetails']
            lender=request.user
            request_id=json_data['request_id']
            borrowrequest_instance=BorrowRequest.objects.get(id=request_id)
            if(borrowrequest_instance.book.quantity < borrowrequest_instance.quantity):
                return JsonResponse({"error": "Requested quantity exceeds available quantity"}, status=400)
            new_rented_instance=Rented.objects.create(
                lender=borrowrequest_instance.lender,
                borrower=borrowrequest_instance.borrower,
                book=borrowrequest_instance.book,
                quantity=borrowrequest_instance.quantity,
                return_date=borrowrequest_instance.return_date
            )
            new_rented_instance.save()
            borrowrequest_instance.status='1'
            borrowrequest_instance.save()
            book=borrowrequest_instance.book
            book.quantity=book.quantity-borrowrequest_instance.quantity
            if(book.quantity==0):
                book.status='1'
            book.save()
            return JsonResponse({"message": "success"})
        except User.DoesNotExist:
            return JsonResponse({"error": "Lender does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def rejectBorrowRequest(request):
    if request.method == 'POST':
        try:
            json_data=request.data['bookDetails']
            request_id=json_data['request_id']
            borrowrequest_instance=BorrowRequest.objects.get(id=request_id)
            borrowrequest_instance.status='2'
            borrowrequest_instance.save()
            return JsonResponse({"message": "success"})
        except User.DoesNotExist:
            return JsonResponse({"error": "Lender does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)