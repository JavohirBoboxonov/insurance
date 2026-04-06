from rest_framework import serializers
from .models import *
import re
import hmac
import hashlib
from django.conf import settings

class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate_phone_number(self, attrs):
        pattern = r' ^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'

        if not re.match(pattern, attrs):
            raise serializers.ValidationError("Invalid phone number")
        
        if not CustomUser.objects.filter(attrs['phone_number'] == self.phone_number).exists():
            raise serializers.ValidationError("Ushbu raqam ro`yxatdan o`tmagan")

        return attrs
        

class TelegramAuthSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    photo_url = serializers.URLField(required=False, allow_blank=True)
    auth_date = serializers.IntegerField()
    hash = serializers.CharField()

    def validate(self, attrs):
        data_check_list = []
        auth_hash = attrs.pop('hash')

        for key, value in sorted(attrs.items()):
            if value:
                data_check_list.append(f"{key}={value}")

        data_check_string = "\n".join(data_check_list)

        secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
        hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if hmac_hash != auth_hash:
            raise serializers.ValidationError("Ma'lumotlar autentifikatsiyadan o'tmadi.")

        return attrs