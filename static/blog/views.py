from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from accounts.choices import UserTypeChoices
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return BlogPost.objects.all()

    def perform_create(self, serializer):
        # Automatically set the owner to the current user
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        # Allow only the owner to update their post
        if self.request.user.user_type == UserTypeChoices.STUDENT and serializer.instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this post, because this is not your post!!!")
        serializer.save()   