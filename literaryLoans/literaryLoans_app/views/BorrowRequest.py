from rest_framework import generics
from ..models import BorrowRequest
from ..serializers import BorrowRequestSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes

class BorrowRequestListAPIView(generics.ListAPIView):
    serializer_class=BorrowRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        queryset = BorrowRequest.objects.filter(lender=user.id).order_by('request_date')
        print("queryset", queryset)
        serializer = BorrowRequestSerializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)    
    
class BorrowRequestStatusListAPIView(generics.ListAPIView):
    serializer_class=BorrowRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        queryset = BorrowRequest.objects.filter(borrower=user.id).order_by('request_date')
        print("queryset", queryset)
        serializer = BorrowRequestSerializer(queryset, many=True)
        print(serializer.data)
        data = serializer.data  # Extract data from the serializer
        for item in data:
            if item['status'] == 1:
                item['status'] = "Accepted"
            elif item['status'] == 2:
                item['status'] = "Cancelled"
            else:
                item['status'] = "Pending"
        return Response(serializer.data)   


        
    



