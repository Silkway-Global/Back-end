from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from accounts.choices import UserTypeChoices
from .filters import TestimonialFilter
from .models import Testimonial
from .serializers import TestimonialSerializer


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = TestimonialFilter

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeChoices.ADMIN:
            return Testimonial.objects.all().order_by('-created_at')
        elif user.user_type == UserTypeChoices.STUDENT:
            return Testimonial.objects.filter(owner=user).order_by('-created_at')
        return Testimonial.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.user_type == UserTypeChoices.STUDENT and serializer.instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this testimonial, because this is not your testimonial!!!")
        serializer.save()

