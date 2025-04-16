from django.shortcuts import render
from rest_framework import viewsets

from accounts.choices import UserTypeChoices
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from rest_framework.permissions import IsAuthenticated  


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeChoices.ADMIN:
            return ContactMessage.objects.all()
        return ContactMessage.objects.none()    