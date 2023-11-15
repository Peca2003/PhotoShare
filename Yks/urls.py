from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
