from rest_framework import generics
from ..models import BorrowRequest
from ..serializers import BorrowRequestSerializer

class BorrowRequestListAPIView(generics.ListAPIView):
    serializer_class=BorrowRequestSerializer

    def get_queryset(self):
        request=self.request
        return BorrowRequest.objects.filter(borrower_id=request.user).filter(status='0')
        
