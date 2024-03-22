from rest_framework import generics
from ..models import Rented
from ..serializers import RentedSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes

class BorrowedbooksListAPIView(generics.ListAPIView):
    serializer_class=RentedSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        queryset = Rented.objects.filter(borrower=user.id).order_by('return_date')
        serializer = RentedSerializer(queryset, many=True)
        return Response(serializer.data)    

