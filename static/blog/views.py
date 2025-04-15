from django.shortcuts import render
from rest_framework import viewsets
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.permissions import IsAuthenticated


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = (IsAuthenticated,)
