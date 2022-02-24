from django.urls import path
from . import views

app_name = 'posts-api'


urlpatterns = [
    path('',views.posts,name="posts"),
    path('create/',views.create_post,name="post-create"),
    path('edit/<str:pk>/', views.edit_post, name="post-edit"),
    path('delete/<str:pk>/', views.delete_post, name="delete-post"),
    path('details/<str:pk>/', views.post_details, name="post-details"),
    path('react/', views.update_react, name="posts-react"),
    path('<str:pk>/comments/', views.post_comments, name="post-comments"),

]