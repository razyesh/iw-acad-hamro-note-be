from .posts import *
from ..models import Comment
from ..serializers import CommentSerializer
from ..paginations import CustomCommentsPagination


class ListComments(ListAPIView):
    """
    This view returns gives the five comments at a time.
    """
    http_method_names = [u'get', ]
    serializer_class = CommentSerializer
    pagination_class = CustomCommentsPagination

    def get_queryset(self):
        return Comment.objects.all()

