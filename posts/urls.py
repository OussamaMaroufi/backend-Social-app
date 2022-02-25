from django.urls import path
from . import views

app_name = 'posts-api'


urlpatterns = [
    path('',views.posts,name="posts"),
    path('create/',views.create_post,name="post-create"),
    path('edit/<str:pk>/', views.edit_post, name="post-edit"),
    path('delete/<str:pk>/', views.delete_post, name="delete-post"),
    path('details/<str:pk>/', views.post_details, name="post-details"),
    path('react/<str:pk>/', views.update_react, name="posts-react"),
    # path('<str:pk>/comments/', views.post_comments, name="post-comments"),
    path('<str:pk>/comments/',views.getComments,name="post-comment"),
    path('<str:pk>/comment-create/',views.create_comment,name="comment-create"),
    path('<str:pk>/comment-delete/',views.delete_comment,name="comment-delete"),
    path('<str:pk>/comment-edit/',views.edit_comment,name="comment-edit"),


]