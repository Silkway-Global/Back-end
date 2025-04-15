from rest_framework import viewsets
from .models import Testimonial
from .serializers import TestimonialSerializer
from rest_framework.permissions import IsAuthenticated


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = (IsAuthenticated,)