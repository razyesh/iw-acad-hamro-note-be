import uuid

from django.utils.text import slugify
from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     UpdateAPIView, RetrieveDestroyAPIView)
from rest_framework.response import Response
from rest_framework import status

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

    def create(self, request, *args, **kwargs):
        """
        The original function overridden so that the post slug is generated
        automatically and is unique.
        """
        data = request.data.copy()
        # copying the dict because the original QueryDict is immutable.

        data['post_slug'] = f'{slugify(data["caption"][:10])}-{uuid.uuid4().hex}'
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


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
