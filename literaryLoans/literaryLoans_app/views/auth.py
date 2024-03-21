# views.py

import os
import requests
import json
from decouple import config
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from literaryLoans_app.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from literaryLoans_app.serializers import UserSerializer
from rest_framework.decorators import api_view

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
        print(code)
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
    user_url = config('GOOGLE_USER_URL')  # Retrieve the user URL from environment variables
    user_url += access_token
    if access_token:
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(user_url, headers=headers)

            # Check for network-related errors
            response.raise_for_status()
            if response.status_code == 200:
                response_data = response.json()
                print("response data", response_data)
                email = response_data['email']
        
                try:
                    email = response_data['email']
                    parts = email.split("@")
                    username = parts[0]
                    print("email", email)
                    existing_user = User.objects.get(email = email)
                    existing_user.email = email
                    existing_user.first_name = response_data['given_name']
                    existing_user.last_name = response_data['family_name']
                    existing_user.picture = response_data['picture']
                    existing_user.username = username
                    existing_user.save()
            
                except:
                    print("except")
                    parts = email.split("@")
                    username = parts[0]
                    new_user = User.objects.create(
                        email = response_data['email'],
                        first_name = response_data['given_name'],
                        last_name = response_data['family_name'],
                        picture = response_data['picture'],
                        username = username
                    )
                    print("new_user", new_user)
                    new_user.save()
                    token = Token.objects.create(user=new_user)

                user = User.objects.get(email = email)   
                token = Token.objects.get(user = user)
                user_data = UserSerializer(user)
                data = user_data.data
                token_str = "Token "
                token_str += token.key
                data["token"] = token_str
                return JsonResponse(data)
            
            else:
                return JsonResponse({'error': 'Request failed due to status code :'}, response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            return JsonResponse({'error': 'Error fetching user data: ' + str(e)}, status=500)
        except ValueError:
            # Handle invalid JSON response
            return JsonResponse({'error': 'Invalid JSON response from user API'}, status=500)
    else:
        # Access token not found in cookie
        return JsonResponse({'error': 'Access token not found'}, status=401)
    
  
@api_view(['POST'])
def onboarding(request):
    if request.method == 'POST':
        # Parse request body to get addressline1, addressline2, city, state, country, and email
        data = request.data['details']
        print("data", data)
        # Access the 'code' key from the JSON data
        addressline1 = data['addressline1']
        addressline2 = data['addressline2']
        city = data['city']
        state = data['state']
        country = data['country']
        email = data['email']
        phoneNumber = data['phoneNumber']
        
        print(email)

        # Check if email is provided
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        # Update user model with provided information
        try:
            user = User.objects.get(email=email)
            user.addressLine1 = addressline1
            user.addressLine2 = addressline2
            user.city = city
            user.state = state
            user.country = country
            user.phone_no = phoneNumber
            user.isOnboarded = True
            user.save()
            return JsonResponse({'message': 'User details updated successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    #take addressline1 , 2, city, state, country, email from body and update user model with given email