# views.py

import os
import requests
from decouple import config
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def google_token(request):
    if request.method == 'POST':
        # Get the values from the .env file
        client_id = config('GOOGLE_CLIENT_ID')
        client_secret = config('GOOGLE_CLIENT_SECRET')
        redirect_uri = config('GOOGLE_REDIRECT_URL')

        # Get the authorization code from the request body
        code = request.POST.get('code')

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
        token_info = response.json()

        # Check if the access token was successfully obtained
        if 'access_token' in token_info:
            # Set the access token as a cookie (secure your cookies in production)
            response = JsonResponse({'status': 'success'})
            response.set_cookie('google_access_token', token_info['access_token'], httponly=True)
            return response
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to get access token'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})