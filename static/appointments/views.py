from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied

from accounts.choices import UserTypeChoices
from .models import Appointment, Consultation
from .serializers import AppointmentSerializer, ConsultationSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == UserTypeChoices.ADMIN:
            return Appointment.objects.all().order_by('-preferred_date')
        elif user.is_authenticated and user.user_type == UserTypeChoices.STUDENT:
            return Appointment.objects.filter(owner=user).order_by('-preferred_date')
        return Appointment.objects.none()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        # if the user is a student and the appointment is not theirs, raise a permission denied error   
        if self.request.user.user_type == UserTypeChoices.STUDENT and serializer.instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this appointment, because this is not your appointment!!")
        serializer.save()


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = (AllowAny,)
