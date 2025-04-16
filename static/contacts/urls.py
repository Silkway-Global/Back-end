from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'contactmessages', ContactMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
