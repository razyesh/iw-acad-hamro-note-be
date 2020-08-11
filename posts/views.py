from django.shortcuts import render

from rest_framework.generics import ListAPIView

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .paginations import CustomPostsPagination, CustomCommentsPagination


class ListPosts(ListAPIView):
    http_method_names = [u'get', ]
    serializer_class = PostSerializer
    pagination_class = CustomPostsPagination

    def get_queryset(self):
        return  Post.objects.all()


class ListComments(ListAPIView):
    http_method_names = [u'get', ]
    serializer_class = CommentSerializer
    pagination_class = CustomCommentsPagination

    def get_queryset(self):
        return Comment.objects.all()
