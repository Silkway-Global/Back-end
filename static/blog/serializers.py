from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 
                  'owner', 
                  'slug', 
                  'title', 
                  'content', 
                  'image', 
                  'created_at', 
                  'updated_at', 
                  'category']
