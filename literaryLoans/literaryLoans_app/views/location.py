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
        # Construct the URL for fetching origins, including the user ID
        origins_api_url = f'http://localhost:8000/address/{user_id}'

        try:
            # Make a GET request to fetch origins
            origins_response = requests.get(origins_api_url)
            origins_response.raise_for_status()  # Raise exception for non-2xx responses
            origins_data = origins_response.json()

            # Extract origins from the response
            origins = '|'.join(', '.join([address['addressLine1'], address['addressLine2'], address['city'], address['state'], address['country']]) for address in origins_data)
            return origins
        except requests.exceptions.RequestException as e:
            # Handle request exceptions
            raise CalculateDistanceException(f"Failed to fetch origins from external API: {e}")

    def get_destinations(self, user_id):
        # Construct the URL for fetching origins, including the user ID
        destinations_api_url = f'http://localhost:8000/destinations/{user_id}'

        try:
            # Make a GET request to fetch origins
            destinations_response = requests.get(destinations_api_url)
            destinations_response.raise_for_status()  # Raise exception for non-2xx responses
            destinations_data = destinations_response.json()

            # Extract origins from the response
            destinations = '|'.join(', '.join([address['addressLine1'], address['addressLine2'], address['city'], address['state'], address['country']]) for address in destinations_data)
            return destinations
        except requests.exceptions.RequestException as e:
            # Handle request exceptions
            raise CalculateDistanceException(f"Failed to fetch origins from external API: {e}")

    def get_distances(self, user_id):
        # Base URL of the external API
        base_url = 'http://api.distancematrix.ai/maps/api/distancematrix/json'

        try:
            # Fetch origins using the helper function
            origins = self.get_origins(user_id)
        except CalculateDistanceException as e:
            return Response({"error": str(e)}, status=500)
        
        try:
            # Fetch origins using the helper function
            destinations = self.get_destinations(user_id)
        except CalculateDistanceException as e:
            return Response({"error": str(e)}, status=500)

        # Retrieve the API key from environment variables
        api_key = os.getenv('API_KEY')
        # print(api_key)
        if not api_key:
            return Response({"error": "API key not found"}, status=500)

        # Construct the complete URL with query parameters
        api_url = f"{base_url}?origins={origins}&destinations={destinations}&key={api_key}"

        try:
            # Make a GET request to the external API
            response = requests.get(api_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract data from the response
                data = response.json()

                # Process the data or return it directly
                return data
            else:
                # Handle other status codes if needed
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
