from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from blog.models import Blog
from .serializers import BlogSerializer

class BlogList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

