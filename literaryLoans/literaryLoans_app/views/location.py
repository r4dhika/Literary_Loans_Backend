# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import os

class CalculateDistance(APIView):
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

    def get(self, request):
        # Base URL of the external API
        base_url = 'http://api.distancematrix.ai/maps/api/distancematrix/json'

        # Retrieve the user ID of the currently logged-in user
        user_id = 1

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
        print(api_key)
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
                return Response(data)
            else:
                # Handle other status codes if needed
                return Response({"error": "Failed to fetch data from external API"}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle connection errors or timeouts
            return Response({"error": str(e)}, status=500)

class CalculateDistanceException(Exception):
    pass

