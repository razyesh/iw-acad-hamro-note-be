from rest_framework.generics import ListAPIView, CreateAPIView

from .models import Post, Comment
from .serializers import (PostSerializer, CommentSerializer,
                          CreatePostSerializer)
from .paginations import CustomPostsPagination, CustomCommentsPagination


class ListPosts(ListAPIView):
    """
    This view is paginated to return a list of 15 posts at a time.
    """
    http_method_names = [u'get', ]
    serializer_class = PostSerializer
    pagination_class = CustomPostsPagination

    def get_queryset(self):
        return Post.objects.all()


class ListComments(ListAPIView):
    """
    This view returns gives the five comments at a time.
    """
    http_method_names = [u'get', ]
    serializer_class = CommentSerializer
    pagination_class = CustomCommentsPagination

    def get_queryset(self):
        return Comment.objects.all()


class CreatePost(CreateAPIView):
    serializer_class = CreatePostSerializer
