from django.urls import path
from . import views
from .views import CustomLoginView, upload_photo
from django.conf import settings
from django.conf.urls.static import static
from .views import profile, edit_profile

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload_photo/', upload_photo, name='upload_photo'),
    path('profile/<str:username>/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('<int:photo_id>/like_photo/', views.like_photo, name='like_photo'),
    path('<int:photo_id>/dislike_photo/', views.dislike_photo, name='dislike_photo'),
    path('<int:photo_id>/add_comment/', views.add_comment, name='add_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
