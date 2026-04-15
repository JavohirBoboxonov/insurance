from rest_framework import serializers
from django.utils import timezone
from .models import Insurance
import re

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'

class InsuranceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'
    def validate_expiry_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("O'tgan sana kiritib bo'lmaydi.")
        return value

    def validate_phone_number(self, value):
        phone_number_regex = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'

        if Insurance.objects.filter(phone_number = value).exists():
            raise serializers.ValidationError('Bu Telefon Raqam Allaqachon Mavjud')

        if not re.match(phone_number_regex, value):
            raise serializers.ValidationError("Bu Format To`g`ri kelmaydi")

        return value

    def validate_car_number(self, attrs):
        if Insurance.objects.filter(car_number = attrs).exists():
            raise serializers.ValidationError('Bu raqam allqachon mavjud')

        car_number_regex = r'^[0-9]{2}[A-Z][0-9]{3}[A-Z]{2}$'

        if not re.match(car_number_regex, attrs):
            raise serializers.ValidationError("Bu format noto`g`ri")
        return attrs
    
    def create(self, validated_data):
        insurance = Insurance.objects.create(
            **validated_data
        )
        return insurance