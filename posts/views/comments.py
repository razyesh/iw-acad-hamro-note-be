from .posts import *
from ..models import Comment
from ..serializers import CommentSerializer, CreateCommentSerializer
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


class CreateComment(CreateAPIView):
    """
    This creates a new comment and saves to the database.
    """
    serializer_class = CreateCommentSerializer


class UpdateComment(UpdateAPIView):
    """
    This should update the comment.
    """
    serializer_class = CreateCommentSerializer

    def get_queryset(self):
        return Comment.objects.all()


class RetrieveDeleteComment(RetrieveDestroyAPIView):
    """
    This retrieves the comment with get request and deletes with delete request.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()
