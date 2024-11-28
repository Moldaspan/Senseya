import datetime
import jwt
from django.conf import settings
from django.core.mail import send_mail
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from google.auth.transport.requests import Request
from google.oauth2.id_token import verify_oauth2_token
from .models import User
from .serializers import UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Генерация токена для активации
        token = jwt.encode({'user_id': user.id}, settings.SECRET_KEY, algorithm='HS256')
        activation_link = f"http://localhost:8000/api/users/activate/{token}"

        # Отправка email
        send_mail(
            subject='Activate Your Account',
            message=f'Click the link to activate your account: {activation_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({'message': 'User registered. Check your email to activate your account.'})


class ActivateUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'message': 'Account activated successfully.'})
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Activation link expired.'}, status=400)
        except jwt.DecodeError:
            return Response({'message': 'Invalid token.'}, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials!')

        if not user.is_active:
            raise AuthenticationFailed('Account is not activated!')

        payload = {
            'id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({'jwt': token})


class ProfileView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'Token is missing or invalid.'}, status=401)

        token = auth_header.split(' ')[1]

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('id')

        return Response({'message': 'Token decoded successfully.', 'user_id': 1})

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'message': 'User not found!'}, status=404)

        # Генерация ссылки сброса пароля
        token = jwt.encode({'user_id': user.id}, settings.SECRET_KEY, algorithm='HS256')
        reset_link = f"http://localhost:8000/api/users/reset-password/{token}"

        send_mail(
            subject='Reset Your Password',
            message=f'Click the link to reset your password: {reset_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({'message': 'Password reset link sent to your email.'})


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        try:
            # Декодирование токена
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')

            # Проверка существования пользователя
            if not user_id:
                return Response({'message': 'Invalid token: no user ID found.'}, status=400)

            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({'message': 'User not found.'}, status=404)

            # Получение нового пароля
            new_password = request.data.get('password')
            if not new_password or len(new_password) < 6:
                return Response({'message': 'Password must be at least 6 characters long.'}, status=400)

            # Установка нового пароля
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password reset successfully.'})
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Reset link expired.'}, status=400)
        except jwt.DecodeError:
            return Response({'message': 'Invalid token.'}, status=400)


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"detail": "Token is required"}, status=400)

        try:
            # Проверка токена
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)

            # Проверяем издателя токена
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise AuthenticationFailed("Invalid issuer")

            # Получение данных пользователя
            email = idinfo.get('email')
            first_name = idinfo.get('given_name')
            last_name = idinfo.get('family_name')

            # Проверка существования пользователя
            user, created = User.objects.get_or_create(email=email, defaults={
                "first_name": first_name,
                "last_name": last_name,
                "is_active": True,  # Активируем пользователя автоматически
            })

            # Генерация JWT токена
            payload = {
                "id": user.id,
                "email": user.email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                "iat": datetime.datetime.utcnow(),
            }
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            return Response({"jwt": jwt_token, "created": created})

        except ValueError:
            return Response({"detail": "Invalid Google token!"}, status=401)
        except Exception as e:
            return Response({"detail": f"Error: {str(e)}"}, status=500)