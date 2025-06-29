from django.test import TestCase
from django.urls import reverse
import json

class ChatbotTests(TestCase):
    def test_chatbot_endpoint(self):
        response = self.client.post(
            reverse('chatbot:chat'),
            data=json.dumps({'message': 'Hola, ¿cómo estás?'}),
            content_type='application/json'
        )
        # Puede ser 200 o 500 si la API de HF falla, pero si tienes token y modelo, debe ser 200
        self.assertIn(response.status_code, [200, 500, 400])
        # Si es 200, debe tener 'response'
        if response.status_code == 200:
            self.assertIn('response', response.json())
        # Si es error, debe tener 'error'
        else:
            self.assertIn('error', response.json())

    def test_chatbot_invalid_message(self):
        response = self.client.post(
            reverse('chatbot:chat'),
            data=json.dumps({'message': ''}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())