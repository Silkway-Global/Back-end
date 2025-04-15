from django.db import models
from accounts.models import CustomUser


class ContactMessage(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.owner.full_name} - {self.subject}"
