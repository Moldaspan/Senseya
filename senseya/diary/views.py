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
        # Получаем список ID для удаления
        entry_ids = request.data.get("entry_ids", [])

        if not entry_ids:
            return Response({"error": "Provide at least one entry ID to delete."}, status=400)

        # Проверяем, что все ID являются целыми числами
        try:
            entry_ids = [int(entry_id) for entry_id in entry_ids]
        except ValueError:
            return Response({"error": "All entry IDs must be integers."}, status=400)

        # Фильтруем записи для текущего пользователя по переданным ID
        entries_to_delete = DiaryEntry.objects.filter(user=request.user, id__in=entry_ids)

        if not entries_to_delete.exists():
            return Response({"error": "No matching diary entries found for the provided IDs."}, status=404)

        # Удаляем записи и возвращаем количество удаленных записей
        deleted_count = entries_to_delete.delete()[0]

        return Response({"message": f"{deleted_count} diary entries deleted successfully."}, status=200)