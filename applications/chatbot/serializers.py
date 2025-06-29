from rest_framework import serializers
from .models import ChatbotMessage

class ChatbotMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotMessage
        fields = ['id', 'user_message', 'bot_response', 'timestamp']