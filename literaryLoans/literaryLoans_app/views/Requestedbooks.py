from rest_framework import generics
from ..models import BorrowRequest
from ..serializers import BorrowRequestSerializer

class RequestedbooksListAPIView(generics.ListAPIView):
    serializer_class=BorrowRequestSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return BorrowRequest.objects.filter(borrower_id=user_id).order_by('-request_date')