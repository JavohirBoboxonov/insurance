from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True
    )
    telegram_id = models.IntegerField(
        blank=True,
        null=True,
        unique = True,
    )
    REQUIRED_FIELDS = ['email', 'phone_number']
    def __str__(self):
        return f"{self.username} = {self.phone_number}"