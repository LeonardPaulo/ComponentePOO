from django.db import models

class Chatbot(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]  # Return the first 50 characters of the question as a string representation

class UserQuery(models.Model):
    user_message = models.TextField()
    chatbot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_message[:50]  # Return the first 50 characters of the user message as a string representation