from django_filters import rest_framework as filters
from .models import Course

class CourseFilter(filters.FilterSet):
    country = filters.CharFilter(field_name='country', lookup_expr='iexact')
    category = filters.CharFilter(field_name='category', lookup_expr='iexact')
    duration_weeks = filters.NumberFilter(field_name='duration_weeks')
    duration_weeks__gte = filters.NumberFilter(field_name='duration_weeks', lookup_expr='gte')
    duration_weeks__lte = filters.NumberFilter(field_name='duration_weeks', lookup_expr='lte')

    class Meta:
        model = Course
        fields = ['country', 'category', 'duration_weeks']
