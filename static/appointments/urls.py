from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
