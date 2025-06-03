from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from accounts.choices import UserTypeChoices
from .models import BlogPost
from .serializers import BlogPostSerializer
from .filters import BlogPostFilter
from .permissions import AdminPostDeleteOnly

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = (AdminPostDeleteOnly,)
    filterset_class = BlogPostFilter

    def get_queryset(self):
        return BlogPost.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.user_type != UserTypeChoices.ADMIN:
            raise PermissionDenied("You do not have permission to edit this post, because this is not your post!!!")
        serializer.save()  