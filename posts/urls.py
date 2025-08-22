from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    path('create/', views.create_post_view, name='create_post'),
    path('<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('<int:post_id>/like/', views.like_post_view, name='like_post'),
    path('<int:post_id>/edit/', views.edit_post_view, name='edit_post'),
    path('<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('my-posts/', views.my_posts_view, name='my_posts'),
    path('images/<str:image_name>/', views.serve_image_view, name='serve_image'),
] 