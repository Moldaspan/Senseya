from google_auth_oauthlib.flow import Flow
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
import os


# Конфигурация для OAuth Flow
GOOGLE_OAUTH2_SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
REDIRECT_URI = "http://localhost:8000/api/users/google/callback"


class GoogleAuthInitView(APIView):
    """
    Инициирует OAuth2 процесс.
    """
    def get(self, request):
        # Инициализируем поток авторизации
        flow = Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "project_id": "senseya",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uris": [REDIRECT_URI],
                }
            },
            scopes=GOOGLE_OAUTH2_SCOPES,
        )
        flow.redirect_uri = REDIRECT_URI

        # Получаем URL для авторизации
        authorization_url, _ = flow.authorization_url(prompt='consent', include_granted_scopes='true')

        return Response({"authorization_url": authorization_url})


class GoogleAuthCallbackView(APIView):
    """
    Обрабатывает callback и возвращает токен.
    """
    def get(self, request):
        # Получаем код авторизации из запроса
        code = request.query_params.get('code')
        if not code:
            return Response({"error": "Authorization code not found!"}, status=400)

        # Настраиваем OAuth flow для получения токена
        flow = Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "project_id": "your-project-id",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uris": [REDIRECT_URI],
                }
            },
            scopes=GOOGLE_OAUTH2_SCOPES,
        )
        flow.redirect_uri = REDIRECT_URI

        try:
            # Обмениваем код на токен
            flow.fetch_token(code=code)
            credentials = flow.credentials

            return Response({
                "access_token": credentials.token,
                "id_token": credentials.id_token,
                "refresh_token": credentials.refresh_token,
                "expires_in": credentials.expiry.isoformat(),
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
