# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from literaryLoans_app.models import User
from literaryLoans_app.serializers import AddressSerializer
from rest_framework.decorators import api_view

class UserDestinations(APIView):
    def get(self, request, user_id):
        # Retrieve all addresses except for the user with the specified user_id
        user_destinations = User.objects.exclude(id=user_id)

        # Serialize the destinations using AddressSerializer
        serializer = AddressSerializer(user_destinations, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def user_addresses(request, user_id):
    # Retrieve the user's addresses or return a 404 if the user doesn't exist
    addresses = User.objects.filter(id=user_id)
    
    if not addresses:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Serialize the addresses using AddressSerializer
    serializer = AddressSerializer(addresses, many=True)
    
    return Response(serializer.data)
