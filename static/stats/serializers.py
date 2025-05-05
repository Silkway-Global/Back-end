# In stats/serializers.py
from rest_framework import serializers

from .models import CourseView

class StudentCountSerializer(serializers.Serializer):
    student_count = serializers.IntegerField()


class CourseViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseView
        fields = ['user', 'course', 'viewed_at']