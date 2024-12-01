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