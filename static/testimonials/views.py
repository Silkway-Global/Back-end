from rest_framework import viewsets
from .models import Testimonial
from .serializers import TestimonialSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.choices import UserTypeChoices

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeChoices.ADMIN:
            return Testimonial.objects.all()
        elif user.user_type == UserTypeChoices.STUDENT:
            return Testimonial.objects.filter(owner=user)
        return Testimonial.objects.none()
