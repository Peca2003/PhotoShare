from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.db.models import Count

from .forms import RegistrationForm, UserLoginForm, PhotoUploadForm
from .models import Photo, UserProfile


def home(request):
    # Получаем последние фотографии с подсчетом лайков и дизлайков для каждой фотографии
    latest_photos = Photo.objects.annotate(num_likes=Count('likes'), num_dislikes=Count('dislikes')).order_by(
        '-created_at')[:10]

    # Получаем популярных пользователей (пример: первые 5 пользователей с наибольшим количеством лайков)
    popular_users = UserProfile.objects.annotate(num_likes=Count('user__photo__likes')).order_by('-num_likes')[:5]

    context = {
        'photos': latest_photos,
        'popular_users': popular_users,
    }

    return render(request, 'Yks/home.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = UserLoginForm


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('home')
    else:
        form = PhotoUploadForm()
    return render(request, 'Yks/upload_photo.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')
