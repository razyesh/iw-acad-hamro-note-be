from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     UpdateAPIView, RetrieveDestroyAPIView)

from ..models import Post
from ..serializers import (PostSerializer, CreatePostSerializer)
from ..paginations import CustomPostsPagination


class ListPosts(ListAPIView):
    """
    This view is paginated to return a list of 15 posts at a time.
    """
    http_method_names = [u'get', ]
    serializer_class = PostSerializer
    pagination_class = CustomPostsPagination

    def get_queryset(self):
        return Post.objects.all()


class CreatePost(CreateAPIView):
    """
    Creates a New Post
    """
    serializer_class = CreatePostSerializer


class UpdatePost(UpdateAPIView):
    """
    Retrieves and updates a new post with post_slug as url kwarg.
    """
    lookup_field = 'post_slug'
    lookup_url_kwarg = 'post_slug'
    serializer_class = CreatePostSerializer

    def get_queryset(self):
        return Post.objects.all()


class RetrieveDeletePost(RetrieveDestroyAPIView):
    """
    Deletes the post with matching post_slug in url kwarg.
    """
    lookup_field = 'post_slug'
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()
