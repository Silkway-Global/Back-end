from rest_framework import serializers

from .models import Appointment

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

