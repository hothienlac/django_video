from django.urls import path
from .views import DeleteVideoView, VideoView, StreamVideoView

urlpatterns = [
    path('', VideoView.as_view(), name='video'),
    path('<str:filename>', StreamVideoView.as_view(), name='video-detail'),
    path('delete/<str:filename>', DeleteVideoView.as_view(), name='video-delete'),
]
