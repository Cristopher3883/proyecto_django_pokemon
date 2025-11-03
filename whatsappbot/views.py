from django.shortcuts import render
import requests
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

VERIFY_TOKEN = "token123"  
ACCESS_TOKEN = "EAAa5NreBfjoBPxUrZCMFK0Q5dSUSuP7jyALQZCp9kIornxc69MQ37YSy5fF1PhSvgreYlbW6bTJQqMaaGEyBU2Vgyo2kNIg0L3d2DZA6M8Hkvkaah5V5XWxD59XcpcMejPJnCnLmNpWyffN1jS1NzSdOfxNGNSyexEoYfh4U2hgj3FzvhctcNgeVOg8y69V7ZAYqlweCF9uvfn8WAz8nPdZCBFhZAY644ZBGtHJOzZA2d8nijWGwixVeGZCoHefJbgRsCZB8mzlKCXoAaIhGW7ZCrET"

# Verificación inicial del webhook (Meta la hace una sola vez)
def webhook_verify(request):
    if request.method == 'GET':
        verify_token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if verify_token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse('Error: token incorrecto', status=403)
    return HttpResponse('Método no permitido', status=405)

# Procesamiento de mensajes entrantes
@csrf_exempt
def webhook_message(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        try:
            messages = data['entry'][0]['changes'][0]['value']['messages']
            for message in messages:
                from_number = message['from']
                text = message.get('text', {}).get('body', '')
                
                # Procesa el mensaje
                responder_whatsapp(from_number, f"Recibido: {text}")
        except KeyError:
            pass
        return HttpResponse("EVENT_RECEIVED")
    else:
        return HttpResponse('Método no permitido', status=405)

# Función para enviar mensajes
def responder_whatsapp(to, message):
    url = f"https://graph.facebook.com/v22.0/876293922230065/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=data)       
    
def respuesta(message):
    pass