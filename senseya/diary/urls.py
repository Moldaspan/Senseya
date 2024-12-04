from django.urls import path
from .views import DiaryListView, DeleteDiaryEntriesView

urlpatterns = [
    path('entries/', DiaryListView.as_view(), name='diary-entries'),
    path('entries/delete/', DeleteDiaryEntriesView.as_view(), name='delete-diary-entries'),
]
