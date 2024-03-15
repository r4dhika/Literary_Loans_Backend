from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models import User
from ..serializers import UserSerializer

class UserDetailAPIView(generics.RetrieveAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class=UserSerializer
    lookup_field = 'id'