from rest_framework import serializers
from datetime import timezone
from .models import Insurance

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'

class InsuranceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = [
            'name',
            'last_name', 
            'middle_name',
            'phone_number',
            'car_number',
            'expiry_date',
        ]

    def validate_expiry_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("O'tgan sana kiritib bo'lmaydi.")
        return value

    def validate_phone_number(self, value):
        if not value.replace('+', '').isdigit():
            raise serializers.ValidationError("Faqat raqam bo'lishi kerak.")
        return value

    def create(self, validated_data):
        insurance = Insurance.objects.create(
            **validated_data
        )
        return insurance

class InsuranceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = [
            'name',
            'last_name',
            'middle_name',
            'phone_number',
            'car_number',
            'expiry_date',
        ]
        extra_kwargs = {
            'phone_number': {'required': False},
            'car_number': {'required': False},
        }

    def validate_expiry_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("O'tgan sana kiritib bo'lmaydi.")
        return value
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.car_number = validated_data.get('car_number', instance.car_number)
        instance.expiry_date = validated_data.get('expiry_date', instance.expiry_date)
        instance.save()
        return instance