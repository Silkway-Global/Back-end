from django_filters import rest_framework as filters

from .models import Testimonial

class TestimonialFilter(filters.FilterSet):
    university = filters.CharFilter(field_name='university', lookup_expr='iexact')

    class Meta:
        model = Testimonial
        fields = ['university']
