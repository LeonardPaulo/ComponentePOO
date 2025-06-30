from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import cohere
from deep_translator import GoogleTranslator

COHERE_API_KEY = "Reemplazar"  # Reemplaza con tu API Key de Cohere

co = cohere.Client(COHERE_API_KEY)

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)
            if len(user_message.split()) > 50:
                return JsonResponse({'error': 'El mensaje no puede tener más de 50 palabras.'}, status=400)

            response = co.generate(
                model="command",
                prompt=user_message,
                max_tokens=200
            )
            response_text = response.generations[0].text.strip()

            # Traducir la respuesta al español usando deep-translator
            traduccion = GoogleTranslator(source='auto', target='es').translate(response_text)

            return JsonResponse({'response': traduccion, 'model': 'cohere-command'})
        except Exception as e:
            print("ERROR EN CHATBOT:", e)
            return JsonResponse({'error': str(e)}, status=500)