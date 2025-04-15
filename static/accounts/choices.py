from django.db import models

class UserTypeChoices(models.TextChoices):
    STUDENT = 'student', 'Student'
    ADMIN = 'admin', 'Admin'
    PARTNER = 'partner', 'Partner'
