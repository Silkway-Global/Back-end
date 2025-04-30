from django.db import models

class CourseCategoryChoices(models.TextChoices):
    LANGUAGE = "language", "Language"
    PREPARATION = "preparation", "Preparation for Admission"


