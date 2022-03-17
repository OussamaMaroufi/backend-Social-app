from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


app_name = 'users-api'

urlpatterns = [

    path('', views.users, name='users'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('recommended/', views.users_recommended, name="users-recommended"),
    path('following/', views.following, name='following'),
    path('<str:username>/follow/', views.follow_user, name="follow-user"),
    path('delete-profile/', views.delete_user, name="delete-user"),
    path('profile/', views.profile, name='profile'),
    path('<str:username>/', views.user, name="user"),
    path('delete-profile/', views.delete_user, name="delete-user"),
    path('profile_update/delete/', views.ProfilePictureDelete,
         name="profile_delete_photo"),
    path('password/change/', views.password_change, name="password-change"),
    path('<str:username>/posts/',views.user_posts , name="user-posts")






]
