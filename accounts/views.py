from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from .models import UserProfile, UserAudio
from .forms import RegisterForm, LoginForm

signer = TimestampSigner()


def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
            UserProfile.objects.create(user=user)

            token = signer.sign(user.pk)
            verify_url = request.build_absolute_uri(reverse('accounts:verify_email', args=[token]))

            send_mail('Verify your email', f'Click to verify: {verify_url}', None, [email])

            return render(request, 'accounts/verification_sent.html', {'email': email})
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request, token):
    try:
        unsigned = signer.unsign(token, max_age=60 * 60 * 24)
        user_pk = int(unsigned)
    except SignatureExpired:
        return render(request, 'accounts/verify_failed.html', {'reason': 'expired'})
    except BadSignature:
        return render(request, 'accounts/verify_failed.html', {'reason': 'bad'})

    user = User.objects.filter(pk=user_pk).first()
    if not user:
        return render(request, 'accounts/verify_failed.html', {'reason': 'notfound'})

    user.is_active = True
    user.save()

    messages.success(request, 'Email verified. You can now log in.')
    return redirect('accounts:login')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('accounts:home')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:home')


@login_required
def audio_page(request):
    UserProfile.objects.get_or_create(user=request.user)
    audios = UserAudio.objects.filter(user=request.user).order_by("-uploaded_at")

    if request.method == "POST":
        action = request.POST.get("action")
        audio_file = request.FILES.get("audio")
        audio_id = request.POST.get("audio_id")

        if action == "upload" and audio_file:
            UserAudio.objects.create(user=request.user, file=audio_file)

        elif action == "replace" and audio_id and audio_file:
            audio_obj = get_object_or_404(UserAudio, id=audio_id, user=request.user)
            audio_obj.file.delete(save=False)
            audio_obj.file = audio_file
            audio_obj.save()

        return redirect("accounts:audio")

    return render(request, "accounts/audio.html", {"audios": audios})


@login_required
def delete_audio(request, audio_id):
    audio_obj = get_object_or_404(UserAudio, id=audio_id, user=request.user)
    audio_obj.file.delete(save=False)
    audio_obj.delete()
    messages.success(request, "Audio deleted successfully!")
    return redirect("accounts:audio")
