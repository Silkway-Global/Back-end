from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import CustomUser


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
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            user_type=validated_data['user_type']
        )

        return user