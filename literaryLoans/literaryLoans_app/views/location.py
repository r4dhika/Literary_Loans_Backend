# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from literaryLoans_app.models import User
from literaryLoans_app.models import Book
from literaryLoans_app.serializers import AddressSerializer, BookSerializer
import requests
import os
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class CalculateDistance(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_origins(self, user_id):
        origins_api_url = f'http://localhost:8000/address/{user_id}'

        try:
            origins_response = requests.get(origins_api_url)
            origins_response.raise_for_status()  
            origins_data = origins_response.json()

            origins = '|'.join(', '.join([
            address.get('addressLine1', ''),
            address.get('addressLine2', ''),
            address.get('city', ''),
            address.get('state', ''),
            address.get('country', '')])
            for address in origins_data if address.get('isOnboarded') == True)
            return origins
        except requests.exceptions.RequestException as e:
            raise CalculateDistanceException(f"Failed to fetch origins from external API: {e}")

    def get_destinations(self, user_id):
        destinations_api_url = f'http://localhost:8000/destinations/{user_id}'

        try:
            destinations_response = requests.get(destinations_api_url)
            destinations_response.raise_for_status()  
            destinations_data = destinations_response.json()

            destinations = '|'.join(', '.join([
            address.get('addressLine1', ''),
            address.get('addressLine2', ''),
            address.get('city', ''),
            address.get('state', ''),
            address.get('country', '')])
            for address in destinations_data if address.get('isOnboarded') == True)
            return destinations
        except requests.exceptions.RequestException as e:
            raise CalculateDistanceException(f"Failed to fetch origins from external API: {e}")

    def get_distances(self, user_id):
        base_url = 'http://api.distancematrix.ai/maps/api/distancematrix/json'

        try:
            origins = self.get_origins(user_id)
        except CalculateDistanceException as e:
            return Response({"error": str(e)}, status=500)
        
        try:
            destinations = self.get_destinations(user_id)
        except CalculateDistanceException as e:
            return Response({"error": str(e)}, status=500)

        api_key = os.getenv('API_KEY')
        if not api_key:
            return Response({"error": "API key not found"}, status=500)

        api_url = f"{base_url}?origins={origins}&destinations={destinations}&key={api_key}"

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()

                return data
            else:
                return Response({"error": "Failed to fetch data from external API"}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle connection errors or timeouts
            return Response({"error": str(e)}, status=500)
        
    def get(self, request):
        user = request.user
        print("user", user)
        api_response = self.get_distances(user.id)

        if api_response.get('status') != 'OK':
            return Response({"error": "Failed to calculate distances"}, status=500)

        distances = [element['distance']['value'] for element in api_response['rows'][0]['elements']]
        users = User.objects.exclude(id = user.id)
        serializer = AddressSerializer(users, many=True)

        sorted_users = [(distance, data) for distance, data in zip(distances, serializer.data)]
        sorted_users.sort(key=lambda x: x[0])
        print(sorted_users)
        serialized_books_list = []
        for user in sorted_users:
            user_books = Book.objects.filter(lender_id=user[1]['id'])
            serializer = BookSerializer(user_books, many=True)
            serialized_books_list.extend(serializer.data)
        return Response(serialized_books_list)


class CalculateDistanceException(Exception):
    pass
