from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    action = models.CharField(max_length=255)  # Описание действия
    timestamp = models.DateTimeField(auto_now_add=True)  # Время действия
    request_method = models.CharField(max_length=10)  # GET, POST, PUT и т.д.
    endpoint = models.CharField(max_length=255)  # URL, куда был запрос
    request_data = models.JSONField(null=True, blank=True)  # Данные запроса
    response_data = models.JSONField(null=True, blank=True)  # Данные ответа
    user_query = models.TextField(null=True, blank=True)  # Запрос пользователя

    def __str__(self):
        return f"Action by {self.user.email} on {self.endpoint} at {self.timestamp}"
