from rest_framework import generics
from ..models import Rented
from ..serializers import RentedSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class LendedbooksListAPIView(generics.ListAPIView):
    serializer_class=RentedSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        user = request.user
        queryset = Rented.objects.filter(lender=user).order_by('return_date')
        serializer = RentedSerializer(queryset, many=True)
        return Response(serializer.data)  
    