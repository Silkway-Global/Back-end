from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 
                  'full_name', 
                  'email', 
                  'password', 
                  'phone_number', 
                  'user_type', 
                  'created_at']
    
        extra_kwargs = {
                'password': {'write_only': True, 'required': True},
                'email': {'required': True}
            }
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  

        user = CustomUser.objects.create(
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user