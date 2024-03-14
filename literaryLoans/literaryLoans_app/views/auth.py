# views.py

import os
import requests
import json
from decouple import config
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def google_token(request):
    if request.method == 'POST':
        # Get the values from the .env file
        client_id = config('GOOGLE_CLIENT_ID')
        # print(client_id)
        client_secret = config('GOOGLE_CLIENT_SECRET')
        redirect_uri = config('GOOGLE_REDIRECT_URL')
        request_body = request.body
        # Get the authorization code from the request body
        json_data = json.loads(request_body.decode('utf-8'))

        # Access the 'code' key from the JSON data
        code = json_data['code']

        # Exchange the authorization code for an access token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }

        response = requests.post(token_url, data=token_data)
        # print(response)
        token_info = response.json()
        # print(token_info)

        # Check if the access token was successfully obtained
        if 'access_token' in token_info:
            # Set the access token as a cookie (secure your cookies in production)
            response = JsonResponse({'status': 'success'})
            # print(token_info)
            response.set_cookie('google_access_token', token_info['access_token'], httponly=True)
            return response
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to get access token'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def user_data(request):
    access_token = request.COOKIES.get('google_access_token')
    print(access_token)
    user_url = config('GOOGLE_USER_URL')  # Retrieve the user URL from environment variables

    if access_token:
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(user_url, headers=headers)

            # Check for network-related errors
            response.raise_for_status()

            user_data = response.json()
            return JsonResponse(user_data)
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            return JsonResponse({'error': 'Error fetching user data: ' + str(e)}, status=500)
        except ValueError:
            # Handle invalid JSON response
            return JsonResponse({'error': 'Invalid JSON response from user API'}, status=500)
    else:
        # Access token not found in cookie
        return JsonResponse({'error': 'Access token not found'}, status=401)