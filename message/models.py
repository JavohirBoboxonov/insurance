from django.db import models
from datetime import datetime

# Create your models here.
class Sms(models.Model):
    from_user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey('insurance.Insurance', on_delete=models.CASCADE, related_name='to_user')
    message = models.TextField()
    text_message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.to_user.name