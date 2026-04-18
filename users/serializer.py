import re
from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        models = CustomUser

class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        
        if not CustomUser.objects.filter(phone_number = attrs['phone_number']).exists():
            raise serializers.ValidationError("This phone number is is not exits")

        user = authenticate(
            username=attrs['phone_number'],
            password=attrs['password']
        )
        
        if not user:
            raise serializers.ValidationError("This user is not exits")
        
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
            raise serializers.ValidationError("This Format is Invalid")
        
        if not CustomUser.objects.filter(phone_number = value).exists():
            raise serializers.ValidationError("This phone number is not exits")
        
        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        
        password_checker = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$'

        if new_password != confirm_password:
            raise serializers.ValidationError("This password and the confirmation password must be the same.")
        
        if not re.match(password_checker, new_password):
            raise serializers.ValidationError("This Password must be standarts")
        
        return attrs
    
    def save(self, **kwargs):
        self.validated_data.pop('confirm_password')
        new_password = self.validated_data.get('new_password')
        phone_number = self.validated_data.get('phone_number')
        user = CustomUser.objects.get(phone_number=phone_number)
        user.set_password(new_password)
        user.save()
        return user