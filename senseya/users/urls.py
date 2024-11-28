from django.urls import path
from .views import (
    RegisterView, ActivateUserView, LoginView,
    ProfileView, ForgotPasswordView, ResetPasswordView,GoogleSignInView
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('activate/<str:token>', ActivateUserView.as_view(), name='activate'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<str:token>', ResetPasswordView.as_view(), name='reset-password'),
    path('google-login', GoogleSignInView.as_view(), name='google-login'),
]
