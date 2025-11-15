from django.contrib import admin
from .models import UserProfile, UserAudio


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(UserAudio)
class UserAudioAdmin(admin.ModelAdmin):
    list_display = ("user", "file", "uploaded_at")
    search_fields = ("user__username", "file")
    list_filter = ("uploaded_at",)
