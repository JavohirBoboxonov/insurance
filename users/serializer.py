import re
import hmac
import hashlib
from rest_framework import serializers
from .models import *
from django.conf import settings
from django.contrib.auth import authenticate

class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'

        if not re.match(pattern, attrs['phone_number']):
            raise serializers.ValidationError("Invalid phone number")
        
        if not CustomUser.objects.filter(phone_number = attrs['phone_number']).exists():
            raise serializers.ValidationError("Ushbu raqam ro`yxatdan o`tmagan")
    
        pass_pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$'

        if not re.match(pass_pattern, attrs):
            raise serializers.ValidationError("Ushbu parol havfsiz emas")

        user = authenticate(phone_number = attrs['phone_number'], password = attrs['password'])
        
        if not user:
            raise serializers.ValidationError("This user none")
        
        if not user.is_active:
            raise serializers.ValidationError('This User is not active')
        
        attrs['user'] = user

        return attrs

class RecoveryPassword(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    def validate_phone_number(self, value):
        phone_number = value

        phone_pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
        if not re.match(phone_pattern, phone_number):
            raise serializers.ValidationError("bu format noto`g`ri")
        
        if not CustomUser.objects.filter(phone_number = value).exists():
            raise serializers.ValidationError("bu telefon raqam mavju emas")
        
        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        
        password_checker = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$'

        if new_password != confirm_password:
            raise serializers.ValidationError("bu parol va tasdiqlash paroli bir xil bo`lishi kerak")
        
        if not re.match(password_checker, new_password):
            raise serializers.ValidationError("bu parol standartlarga mos kelmaydi")
        
        return attrs
    
    def save(self, **kwargs):
        self.validated_data.pop('confirm_password')
        new_password = self.validated_data.get('new_password')
        phone_number = self.validated_data.get('phone_number')
        user = CustomUser.objects.get(phone_number=phone_number)
        user.set_password(new_password)
        user.save()
        return user


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