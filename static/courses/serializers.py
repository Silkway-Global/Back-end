from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id',
                  'owner',
                  'title', 
                  'description', 
                  'duration_weeks', 
                  'price', 
                  'country', 
                  'category', 
                  'start_date', 
                  'image',]
        extra_kwargs = {
                'owner': {'read_only': True}
            }
