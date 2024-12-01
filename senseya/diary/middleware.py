import json
from django.utils.timezone import now
from .models import DiaryEntry


class DiaryLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Сохраняем действия только для авторизованных пользователей
        if request.user.is_authenticated:
            DiaryEntry.objects.create(
                user=request.user,
                action=f"{request.method} {request.path}",
                timestamp=now(),
                request_method=request.method,
                endpoint=request.path,
                request_data=self.get_request_data(request),
                response_data=self.get_response_data(response)
            )
        return response

    def get_request_data(self, request):
        try:
            return json.loads(request.body) if request.body else {}
        except Exception:
            return {}

    def get_response_data(self, response):
        try:
            return json.loads(response.content) if response.content else {}
        except Exception:
            return {}
