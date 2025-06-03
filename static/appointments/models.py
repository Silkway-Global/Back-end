from django.db import models

from accounts.models import CustomUser


class Appointment(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment with {self.owner.full_name} on {self.preferred_date} at {self.preferred_time}"
