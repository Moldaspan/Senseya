from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.email} - {self.query[:30]}"
