from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from .models import CustomUser
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated

class CustomUserThrotle(UserRateThrottle):
    rate = '5/minute'

class Login(APIView):
    throttle_classes = [CustomUserThrotle]

    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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
            
class SignOut(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Muvaqiyatli log out qilindi"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
        
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