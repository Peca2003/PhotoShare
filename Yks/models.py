from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')
    bio = models.TextField(blank=True, null=True)
    # Добавьте другие поля профиля пользователя, если необходимо


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_photo', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_photo', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    photo = models.ForeignKey(Photo, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)