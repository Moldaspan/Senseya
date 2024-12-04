from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatSession


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        query = request.data.get("query", "")

        if not query:
            return Response({"error": "Query is required"}, status=400)

        # Генерация ответа (здесь можно подключить AI-логику)
        system_response = self.generate_response(query)

        # Сохранение в дневник (ChatSession)
        chat_entry = ChatSession.objects.create(
            user=user,
            query=query,
            response=system_response
        )

        # Возвращение ответа пользователю
        return Response({
            "user_query": chat_entry.query,
            "system_response": chat_entry.response,
            "timestamp": chat_entry.timestamp
        })

    def generate_response(self, query):
        # Пример генерации ответа
        if "AI" in query:
            return "AI stands for Artificial Intelligence."
        elif "machine learning" in query:
            return "Machine learning is a subset of AI that focuses on data learning."
        else:
            return "Sorry, I can't help with that."
