# views.py
from rest_framework import generics, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Blog
from .serializers import BlogListSerializer


class CustomPagination(LimitOffsetPagination):
    default_limit = 1
    max_limit = 10


class BlogListingView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    pagination_class = CustomPagination
