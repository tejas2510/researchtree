from django.urls import path
from . import views
from .views import create_superuser  # ← this line was probably missing
from .views import reset_admin_password  # 🛠️ THIS is the important line

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('create-superuser/', create_superuser, name='create_superuser'),
    path('reset-admin-password/', reset_admin_password, name='reset_admin_password'),
]
