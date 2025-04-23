from rest_framework import serializers
from .models import Testimonial

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 
                  'owner', 
                  'university', 
                  'story', 
                  'photo', 
                  'video_url', 
                  'country', 
                  'created_at', 
                  'updated_at']
        extra_kwargs = {
                'owner': {'read_only': True}
            }
