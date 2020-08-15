from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [

    path('post/list/', views.ListPosts.as_view(), name='posts_list'),
    path('post/create/', views.CreatePost.as_view(), name='post_create'),
    # The below url can view and delete the post with get and delete method.
    path('post/<str:post_slug>/', views.RetrieveDeletePost.as_view(),
         name='post_get_delete'),
    path('post/<str:post_slug>/update/', views.UpdatePost.as_view(),
         name='post_update'),
    # like post api
    path('post/<str:post_slug>/<str:action>/', views.like_post,
         name='like_unlike_post'),
    # comments
    path('comment/list/', views.ListComments.as_view(), name='comment_list'),
    path('comment/create/', views.CreateComment.as_view(),
         name='comment_create'),
    path('comment/<str:pk>/update/', views.UpdateComment.as_view(),
         name='comment_update'),
    path('comment/<str:pk>/', views.RetrieveDeleteComment.as_view(),
         name='comment_get_delete'),
    path('comment/<str:pk>/<str:action>/', views.like_comment,
         name='like_unlike_comment'),
]
