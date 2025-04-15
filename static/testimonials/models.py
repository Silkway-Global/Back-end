from django.db import models
from accounts.models import CustomUser


class Testimonial(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    university = models.CharField(max_length=255)
    story = models.TextField()
    photo = models.ImageField(upload_to='testimonials_photos/')
    video_url = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.owner.full_name} - {self.university}"
