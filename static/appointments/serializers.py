from rest_framework import serializers

from .models import Appointment, Consultation

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 
                  'owner', 
                  'preferred_date', 
                  'preferred_time', 
                  'message', 
                  'created_at']
        extra_kwargs = {
                'owner': {'read_only': True}
            }


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['id', 'full_name', 'phone_number', 'created_at']

