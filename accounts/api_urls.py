from django.urls import path
from . import api_views

urlpatterns = [
    path('users/<int:pk>/', api_views.UserDetailAPIView.as_view(), name='api_user_detail'),
    path('users/<int:pk>/upload_audio/', api_views.UploadAudioAPIView.as_view(), name='api_upload_audio'),
]
