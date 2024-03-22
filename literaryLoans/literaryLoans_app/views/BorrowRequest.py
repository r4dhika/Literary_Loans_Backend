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
from django.core.mail import send_mail

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
            print(json_data)
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
            subject = "New Borrow Request"
            lender_name = lender.first_name + " " + lender.last_name
            book_name = book.title
            borrower_name = borrower.first_name + borrower.last_name
            borrower_email = borrower.email
            print(lender.first_name)
            message = f"""
Dear {lender_name},

We hope this email finds you well. We wanted to inform you that a borrower has requested to borrow the books you have put on lend through our app. We appreciate your participation in our lending community and wanted to ensure that you are aware of this request.

Here are the details of the request:

Requested Book: {book_name}
Borrower's Details:
Name: {borrower_name}
Email: {borrower_email}

Please review this request and let us know if we approve it. You can confirm or deny the request directly through the website by accessing your dashboard.

If you approve the request, we will facilitate the borrowing process and provide you with further instructions. If you deny the request or have any concerns, please don't hesitate to reach out to us.

Thank you for your cooperation and for being part of our lending community. If you have any questions or need assistance, feel free to contact us anytime.

Best regards,

Literary Loans
            """
            print("subject", subject)
            print("message", message)
            recipient_list = [lender.email]
            send_mail(subject, message, None, recipient_list)
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
                book.available = False
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