from django.db import models
from django.utils import timezone

class Insurance(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)

    phone_number = models.CharField(max_length=15, unique=True, db_index=True)
    car_number = models.CharField(max_length=20, unique=True)

    created_at = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()

    @property
    def remaining_days(self):
        if self.expiry_date:
            delta = self.expiry_date - timezone.localdate()
            return max(delta.days, 0)
        return None
    
    @property
    def status(self):
        if not self.expiry_date:
            return "unknown"

        today = timezone.localdate()

        if self.expiry_date >= today:
            return "active"
        return "expired"