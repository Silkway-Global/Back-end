from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestimonialViewSet
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'testimonials', TestimonialViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 

