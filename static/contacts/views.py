from django.shortcuts import render
from rest_framework import viewsets
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from rest_framework.permissions import IsAuthenticated  


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = (IsAuthenticated,)