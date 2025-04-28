from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated  
from rest_framework.exceptions import PermissionDenied

from accounts.choices import UserTypeChoices
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeChoices.ADMIN:
            return ContactMessage.objects.all()
        elif user.user_type == UserTypeChoices.STUDENT:
            return ContactMessage.objects.filter(owner=user)
        return ContactMessage.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.user_type == UserTypeChoices.STUDENT and serializer.instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this message, because this is not your message!!!")


