from django.urls import path
from . import views
from .views import create_superuser  # ← this line was probably missing

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('create-superuser/', create_superuser, name='create_superuser'),
]
