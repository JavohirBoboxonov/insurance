from rest_framework import serializers
from .models import *
import re
import hmac
import hashlib
import hashlib
from django.conf import settings
from django.contrib.auth import authenticate

class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'

        if not re.match(pattern, attrs['phone_number']):
            raise serializers.ValidationError("Invalid phone number")
        
        if not CustomUser.objects.filter(attrs['phone_number'] == self.phone_number).exists():
            raise serializers.ValidationError("Ushbu raqam ro`yxatdan o`tmagan")
    
        pass_pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$'

        if not re.match(pass_pattern, attrs):
            raise serializers.ValidationError("Ushbu parol havfsiz emas")

        user = authenticate(attrs['phone_number', attrs['password']])
        
        if not user:
            raise serializers.ValidationError("This user none")

class TelegramAuthSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    photo_url = serializers.URLField(required=False)
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