from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 
                  'owner', 
                  'subject', 
                  'message', 
                  'sent_at']
