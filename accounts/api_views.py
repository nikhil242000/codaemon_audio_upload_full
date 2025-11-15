from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import UserProfile
from django.contrib.auth.models import User

class UserDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        audio_url = request.build_absolute_uri(profile.audio.url) if profile.audio and hasattr(profile.audio, 'url') else None
        return Response({'id': user.pk, 'username': user.username, 'email': user.email, 'audio_url': audio_url})

class UploadAudioAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        # only allow uploading for the authenticated user's own pk (or admins)
        if request.user.pk != pk and not request.user.is_staff:
            return Response({'detail':'forbidden'}, status=status.HTTP_403_FORBIDDEN)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if 'audio' not in request.FILES:
            return Response({'detail':'audio file required'}, status=status.HTTP_400_BAD_REQUEST)
        f = request.FILES['audio']
        if not f.name.lower().endswith(('.mp3','.wav','.m4a','.ogg')):
            return Response({'detail':'unsupported format'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if profile.audio:
                profile.audio.delete(save=False)
        except Exception:
            pass
        profile.audio = f
        profile.save()
        audio_url = request.build_absolute_uri(profile.audio.url) if profile.audio and hasattr(profile.audio, 'url') else None
        return Response({'detail':'uploaded','audio_url': audio_url})
