import africastalking
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

#Create your credentials
username = "sandbox"
apikey = "973046b36658a8016b85fce904282459a27307efe7b1f5a78e6eaa89cf4c6a40"

africastalking.initialize(username, apikey)

sms = africastalking.SMS

def send_SMS(recipients,message):
    sender = '11336'
    try:
        response = sms.send(message, recipients, sender)
        print(response)
    except Exception as e:
        response = e
        print(f"Houston, we have a problem {e}")
    
    return response

@csrf_exempt
def callback(response):
    return HttpResponse(response)