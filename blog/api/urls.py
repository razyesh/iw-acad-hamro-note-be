from django.urls import path
from .views import BlogList, BlogDetail, CommentList, CommentDetail

urlpatterns = [
    path('v1/listblog/',BlogList.as_view(),name='list_blog'),
    path('v1/blogdetail/<int:pk>/',BlogDetail.as_view(),name='detail_blog'),
    path('v1/listcomment/',CommentList.as_view(),name='list_comment'),
    path('v1/detailcomment/<int:pk>/',CommentDetail.as_view(),name='detail_comment'),
]
