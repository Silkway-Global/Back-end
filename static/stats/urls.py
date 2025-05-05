from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import student_count_view, CourseViewViewSet

router = DefaultRouter()
router.register(r'course-views', CourseViewViewSet)

urlpatterns = [
    path('student-count/', student_count_view, name='student-count'),
    path('', include(router.urls)),
]