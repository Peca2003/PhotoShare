from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User
from .forms import UserProfileForm, RegistrationForm, UserLoginForm, PhotoUploadForm, CommentForm
from .models import Photo, UserProfile, Comment
from django.http import JsonResponse
from datetime import datetime

def home(request):
    # Получаем последние фотографии с подсчетом лайков и дизлайков для каждой фотографии
    latest_photos = Photo.objects.annotate(num_likes=Count('likes'), num_dislikes=Count('dislikes')).order_by(
        '-created_at')
    # Получаем популярных пользователей (пример: первые 5 пользователей с наибольшим количеством лайков)
    popular_users = UserProfile.objects.annotate(num_likes=Count('user__photo__likes')).order_by('-num_likes')[:5]


    return render(request, 'Yks/home.html', {'photos': latest_photos, 'popular_users': popular_users})


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

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    is_owner = user == request.user
    return render(request, 'Yks/profile.html', {'user': user, 'user_profile': user_profile, 'is_owner': is_owner})

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'Yks/edit_profile.html', {'form': form})

@login_required
def like_photo(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    # Проверяем, поставил ли пользователь дизлайк ранее, и если да, то удаляем дизлайк.
    if request.user in photo.dislikes.all():
        photo.dislikes.remove(request.user)

    # Если пользователь уже поставил лайк, не делаем ничего.
    if request.user not in photo.likes.all():
        photo.likes.add(request.user)

    return redirect('home')


@login_required
def dislike_photo(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    # Проверяем, поставил ли пользователь лайк ранее, и если да, то удаляем лайк.
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)

    # Если пользователь уже поставил дизлайк, не делаем ничего.
    if request.user not in photo.dislikes.all():
        photo.dislikes.add(request.user)

    return redirect('home')

@login_required
def add_comment(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    form = CommentForm(instance=photo)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=photo)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['body']
            c = Comment(photo=photo, name=name, body=body, date_added=datetime.now())
            c.save()
            return redirect('home')
        else:
            print('Ошибка')
    else:
        form = CommentForm()
    context = {
        'form': form
    }
    return render(request, 'Yks/add_comment.html', context)

@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    if photo.user == request.user:
        photo.delete()
    return redirect('home')

def user_logout(request):
    logout(request)
    return redirect('home')