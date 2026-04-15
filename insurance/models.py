from django.db import models
from django.utils import timezone

class Insurance(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)

    phone_number = models.CharField(max_length=15, unique=True)
    car_number = models.CharField(max_length=20, unique=True)

    created_at = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(blank=True, null=True)

    @property
    def remaining_days(self):
        if self.expiry_date:
            delta = self.expiry_date - timezone.now()
            return max(delta.days, 0)
        return None