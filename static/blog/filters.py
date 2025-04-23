from django_filters import rest_framework as filters
from .models import BlogPost
from datetime import datetime

class BlogPostFilter(filters.FilterSet):
    created_at = filters.CharFilter(method='filter_created_at')
    created_at__gte = filters.CharFilter(method='filter_created_at_gte')
    created_at__lte = filters.CharFilter(method='filter_created_at_lte')

    class Meta:
        model = BlogPost
        fields = ['created_at']

    def filter_created_at(self, queryset, name, value):
        try:
            date = datetime.strptime(value, '%Y.%m.%d').date()
            return queryset.filter(created_at__date=date)
        except ValueError:
            return queryset.none()

    def filter_created_at_gte(self, queryset, name, value):
        try:
            date = datetime.strptime(value, '%Y.%m.%d').date()
            return queryset.filter(created_at__date__gte=date)
        except ValueError:
            return queryset.none()

    def filter_created_at_lte(self, queryset, name, value):
        try:
            date = datetime.strptime(value, '%Y.%m.%d').date()
            return queryset.filter(created_at__date__lte=date)
        except ValueError:
            return queryset.none()