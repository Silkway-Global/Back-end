from django.db import models
from django.conf import settings
from courses.models import Course
from accounts.models import CustomUser

class CourseView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):  
        return f"{self.user.username} viewed {self.course.id} at {self.viewed_at}"