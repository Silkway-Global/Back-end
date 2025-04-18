from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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
    
    