from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
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
                'message': 'Something is wrong',
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
                "phone_number": user.phone_number,
                "email": user.email
            }
        }, status=status.HTTP_200_OK)
            
class SignOut(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Succesfully logout"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class VerifyApi(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        user = request.user

        return Response({
            "response": "successfull",
            "data": {
                "id": user.id,
                "phone_number": user.phone_number,
                "is_staff": user.is_staff
            }
        }, status=200)

class ProfileView(APIView):
    permission_classes = (IsAuthenticated)
    def get(self, request):
        serializer = ProfileSerializer(data=request.data)
        
        return Response({
            "message": "succesfully",
            "data": serializer.data
        }, status=200)