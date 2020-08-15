from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from blog.models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer

class BlogList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
