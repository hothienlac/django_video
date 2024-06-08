from django.urls import path
from .views import VideoView, StreamVideoView

urlpatterns = [
    path('', VideoView.as_view(), name='video'),
    path('<str:filename>', StreamVideoView.as_view(), name='video-detail'),
]
