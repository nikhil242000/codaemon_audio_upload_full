from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),

    # Audio management
    path('audio/', views.audio_page, name='audio'),
    path('audio/delete/<int:audio_id>/', views.delete_audio, name='delete_audio'),
]
