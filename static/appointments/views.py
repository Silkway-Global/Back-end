from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from accounts.choices import UserTypeChoices

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated,)

    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeChoices.ADMIN:
            return Appointment.objects.all()
        elif user.user_type == UserTypeChoices.STUDENT:
            return Appointment.objects.filter(owner=user)
        return Appointment.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.user_type == UserTypeChoices.STUDENT and serializer.instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this appointment, because this is not your appointment!!!")
