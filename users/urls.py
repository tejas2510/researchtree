from django.urls import path
from . import views

urlpatterns = [
    path('profile-setup/', views.profile_setup, name='profile_setup'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<int:user_id>/', views.profile_view, name='view_user_profile'),
]