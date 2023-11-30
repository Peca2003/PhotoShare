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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
