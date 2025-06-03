from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied

from accounts.choices import UserTypeChoices
from .filters import CourseFilter
from .models import Course
from .serializers import CourseSerializer
from stats.models import CourseView

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (AllowAny,)
    filterset_class = CourseFilter

    def get_queryset(self):
        return Course.objects.all().order_by('-start_date')    
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.user_type == UserTypeChoices.STUDENT and serializer.instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this course, because this is not your course!!!")
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if not CourseView.objects.filter(user=user, course=instance).exists():
            instance.requests += 1
            instance.save()

            CourseView.objects.create(user=user, course_id=instance.id)

        return super().retrieve(request, *args, **kwargs)
