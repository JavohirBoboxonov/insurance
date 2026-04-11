from django.db import models
from django.utils import timezone
# Create your models here.
class Insurance(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True)
    car_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    
    @property
    def remaining_days(self):
        if self.expiry_date:
            delta = self.expiry_date - timezone.now()
            return delta.days
        return None