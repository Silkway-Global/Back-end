from django.shortcuts import render
from accounts.models import CustomUser
from accounts.choices import UserTypeChoices
from django.http import JsonResponse
from rest_framework import viewsets
from .models import CourseView
from .serializers import CourseViewSerializer


# get the number of students    
def student_count_view(request):
    student_count = CustomUser.objects.filter(user_type=UserTypeChoices.STUDENT).count()
    return JsonResponse({'student_count': student_count})


class CourseViewViewSet(viewsets.ModelViewSet):
    queryset = CourseView.objects.all()
    serializer_class = CourseViewSerializer
    
    def retrieve(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        course_views_count = CourseView.objects.filter(course_id=course_id).count()
        return JsonResponse({'course_views_count': course_views_count})
    