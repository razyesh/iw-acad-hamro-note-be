from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('comment/list/', views.ListComments.as_view(), name='comment_list'),
    path('post/list/', views.ListPosts.as_view(), name='posts_list'),
    path('post/create/', views.CreatePost.as_view(), name='post_create'),
    # The below url can view and delete the post with get and delete method.
    path('post/<str:post_slug>/', views.RetrieveDeletePost.as_view(),
         name='post_get_delete'),
    path('post/<str:post_slug>/update/', views.UpdatePost.as_view(),
         name='post_update'),
]
