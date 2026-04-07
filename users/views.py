from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from .models import CustomUser
from rest_framework.throttling import UserRateThrottle

class CustomUserThrotle(UserRateThrottle):
    rate = '5/minutte'

class Login(APIView):

    throttle_classes = [CustomUserThrotle]

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Ma`lumotlar Noto`g`ri',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Succesfully Login",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_data": {
                "id": user.id,
                "phone_number": user.phone_number
            }
        }, status=status.HTTP_400_BAD_REQUEST)
            

class TelegramLogin(APIView):
    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            user, created = CustomUser.objects.get_or_create(
                username = f"tg_{data['id']}",
                defaults={'first_name': data.get('first_name')}
            )

            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "is_new": created
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)