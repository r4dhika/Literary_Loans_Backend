from rest_framework import generics
from ..models import BorrowRequest
from ..serializers import BorrowRequestSerializer

class LendedbooksListAPIView(generics.ListAPIView):
    serializer_class=BorrowRequestSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return BorrowRequest.objects.filter(lender_id=user_id).filter(status='1').order_by('return_date')