from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Photo, UserProfile
from .forms import RegistrationForm, UserLoginForm
from django.contrib.auth.views import LoginView


def home(request):
    # Получаем последние фотографии
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
            return redirect('login')  # Перенаправляем пользователя на страницу входа после успешной регистрации
    else:
        form = RegistrationForm()
    return render(request, 'registrations/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registrations/login.html'  # Путь к шаблону для страницы авторизации
    authentication_form = UserLoginForm

