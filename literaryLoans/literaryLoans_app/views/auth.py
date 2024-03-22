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
from rest_framework.views import APIView
from rest_framework.response import Response

@csrf_exempt
def google_token(request):
    if request.method == 'POST':
        client_id = config('GOOGLE_CLIENT_ID')
        client_secret = config('GOOGLE_CLIENT_SECRET')
        redirect_uri = config('GOOGLE_REDIRECT_URL')
        request_body = request.body
        json_data = json.loads(request_body.decode('utf-8'))

        code = json_data['code']

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
        token_info = response.json()

        if 'access_token' in token_info:
            response = JsonResponse({'status': 'success'})
            response.set_cookie('google_access_token', token_info['access_token'], httponly=True)
            return response
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to get access token'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def user_data(request):
    access_token = request.COOKIES.get('google_access_token')
    user_url = config('GOOGLE_USER_URL') 
    user_url += access_token
    if access_token:
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(user_url, headers=headers)

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
            return JsonResponse({'error': 'Error fetching user data: ' + str(e)}, status=500)
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON response from user API'}, status=500)
    else:
        return JsonResponse({'error': 'Access token not found'}, status=401)
    
  
@api_view(['POST'])
def onboarding(request):
    if request.method == 'POST':
        data = request.data['details']
        print("data", data)
        addressline1 = data['addressline1']
        addressline2 = data['addressline2']
        city = data['city']
        state = data['state']
        country = data['country']
        email = data['email']
        phoneNumber = data['phoneNumber']
        
        print(email)

        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

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


class Logout(APIView):
    def post(self, request):
        response = Response({"message": "Cookie deleted successfully"})
        response.delete_cookie('google_access_token')
        return response
