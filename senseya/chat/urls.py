from django.urls import path
from .views import ChatView

urlpatterns = [
    path('query/', ChatView.as_view(), name='chat'),
]