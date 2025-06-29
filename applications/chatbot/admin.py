from django.contrib import admin
from .models import UserQuery

@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_message', 'chatbot_response', 'timestamp')
    search_fields = ('user_message', 'chatbot_response')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)