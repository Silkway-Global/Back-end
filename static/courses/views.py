from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from accounts.choices import UserTypeChoices
from .filters import CourseFilter
from .models import Course
from .serializers import CourseSerializer
from stats.models import CourseView

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = CourseFilter

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeChoices.ADMIN:
            return Course.objects.all().order_by('-start_date')
        elif user.user_type == UserTypeChoices.STUDENT:
            return Course.objects.filter(owner=user).order_by('-start_date')
        return Course.objects.none()    
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.user_type == UserTypeChoices.STUDENT and serializer.instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this course, because this is not your course!!!")
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        # Check if the user has already viewed the course
        if not CourseView.objects.filter(user=user, course=instance).exists():
            # Increment the requests field
            instance.requests += 1
            instance.save()

            # Record the view
            CourseView.objects.create(user=user, course_id=instance.id)

        return super().retrieve(request, *args, **kwargs)
