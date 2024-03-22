from django.core.mail import send_mail
from django.http import JsonResponse

def EmailAPI(request):
    if request.method == 'GET':
        # Get parameters from the request URL
        subject = request.GET.get('subject', '')
        message = request.GET.get('text', '')
        recipient_list = [request.GET.get('recipient_list', '')]

        # Check if all required parameters are provided
        if subject and message and recipient_list:
            try:
                # Send email
                send_mail(subject, message, None, recipient_list)
                return JsonResponse({'message': 'Email sent successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
