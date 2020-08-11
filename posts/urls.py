from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('comments/list', views.ListComments.as_view(), name='comment_list'),
    path('posts/list', views.ListPosts.as_view(), name='posts_list')
]