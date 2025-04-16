from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 

if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)