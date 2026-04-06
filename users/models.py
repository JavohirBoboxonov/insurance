from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        unique=True
    )
    telegram_id = models.IntegerField(
        blank=True,
        null=True,
        unique = True,
    )

    def __str__(self):
        return f"{self.username} = {self.phone_number}"

class Insurance(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True)
    car_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    @property
    def remaining_days(self):
        if self.expiry_date:
            delta = self.expiry_date - timezone.now().date()
            return delta.days
        return None

    @property
    def is_expiry(self):
        if self.expiry_date:
            return timezone.now().date() > self.expiry_date
        return False

    def __str__(self):
        return f"{self.last_name} {self.name} - {self.car_number}"

    class Meta:
        verbose_name = "Sug`urta"
        verbose_name_plural = "Sug`urtalar"
        ordering = ["-created_at"]