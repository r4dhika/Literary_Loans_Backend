from rest_framework import generics
from ..models import Rented
from ..serializers import RentedSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class LendedbooksListAPIView(APIView):
    serializer_class=RentedSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        return Response(Rented.objects.filter(lender=user).order_by('return_date'))