from django.urls import path
from .views import BlogList, BlogDetail, CommentList, CommentDetail

urlpatterns = [
    path('listblog/',BlogList.as_view(),name='list_blog'),
    path('blogdetail/<int:pk>/',BlogDetail.as_view(),name='detail_blog'),
    path('listcomment',CommentList.as_view(),name='list_comment'),
    path('detailcomment/<int:pk>/',CommentDetail.as_view(),name='detail_comment'),
]
