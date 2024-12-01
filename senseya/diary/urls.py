from django.urls import path
from .views import DiaryListView

urlpatterns = [
    path('entries/', DiaryListView.as_view(), name='diary-entries'),
]
