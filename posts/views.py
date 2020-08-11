from django.shortcuts import render

from rest_framework.generics import ListAPIView

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .paginations import CustomPageNumberPagination


class ListPosts(ListAPIView):
    http_method_names = [u'get']
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination
