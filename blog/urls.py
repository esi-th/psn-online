from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list_view, name='posts_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('like/<int:post_id>/', views.like_post_view, name='like_post'),
    path('create/<int:post_id>', views.CommentCreateView.as_view(), name='comment_create'),
    path('reply/<int:comment_id>/', views.reply_to_comment, name='reply_to_comment'),
]
