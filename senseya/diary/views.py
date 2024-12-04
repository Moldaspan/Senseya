from django.utils.dateparse import parse_datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DiaryEntry


class DiaryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = DiaryEntry.objects.filter(user=request.user).order_by('-timestamp')
        data = [
            {
                "action": entry.action,
                "timestamp": entry.timestamp,
                "request_method": entry.request_method,
                "endpoint": entry.endpoint,
                "request_data": entry.request_data,
                "response_data": entry.response_data,
                "user_query": entry.user_query,
            }
            for entry in entries
        ]
        return Response(data)


class DeleteDiaryEntriesView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        # Получаем параметры фильтрации из запроса
        action = request.data.get("action")  # Удаление по типу действия
        query_text = request.data.get("query")  # Удаление по тексту запроса
        endpoint = request.data.get("endpoint")  # Удаление по endpoint

        # Проверяем, что хотя бы один фильтр указан
        if not any([action, query_text, endpoint]):
            return Response(
                {"error": "Provide at least one filter: action, query, or endpoint."},
                status=400,
            )

        # Фильтруем записи по указанным параметрам
        entries = DiaryEntry.objects.filter(user=request.user)
        if action:
            entries = entries.filter(action=action)
        if query_text:
            entries = entries.filter(request_data__query=query_text)
        if endpoint:
            entries = entries.filter(endpoint=endpoint)

        # Удаляем записи
        count = entries.count()
        entries.delete()

        return Response(
            {"message": f"{count} diary entries deleted successfully."},
            status=200,
        )