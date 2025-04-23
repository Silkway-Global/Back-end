from django.db import models
from accounts.models import CustomUser

class Course(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration_weeks = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    start_date = models.DateField()
    image = models.ImageField(upload_to='course_images/')

    def __str__(self):
        return self.title