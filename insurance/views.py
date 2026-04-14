from rest_framework.views import APIView
from .serializer import *
from django.db.models import Q
from rest_framework import viewsets
from .models import Insurance
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.

class InsuranceCreate(APIView):
    permission_classes = (IsAuthenticated, )

    serializer_class = InsuranceCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({
                "detail": "Ma`lumotlar noto`g`ri kiritilgan",
                "errors": serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        insurance = serializer.validated_data['insurance']

        refresh = RefreshToken(insurance)

        return Response({
            "detail": "Sug`urta yaratildi",
            "data": insurance.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=201)
        
class InsuranceUpdate(APIView):

    serializer_class = InsuranceUpdateSerializer

    def post(self, request):
        serializer = InsuranceUpdate(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                "detail": "Ma`lumotlar no`to`gri",
                "error": serializer.errors
            }, status=400)
        insuranse = serializer.validated_data['insuranse']

        refresh_token = RefreshToken(insuranse)

        return Response({
            "detail": "sug`urta yangilandi",
            "data": insuranse,
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token)
        }, status=201)
        
class InsuranceDelete(APIView):
    def post(self, request):
        insurance_id = request.data.get('id')

        if not insurance_id:
            return Response(
                {"error": "ID yuborilmadi"}
            )
        try:
            insurance = Insurance.objects.get(id=insurance_id)
            insurance.delete()

            return Response({
                "message": "Sug`urta muvaqiyatli o`chirildi"
            }, status=status.HTTP_200_OK)
        except Insurance.DoesNotExist:
            return Response(
                {"error": "Bunday ID dagi sug`urta toopilmadi"},
                status=status.HTTP_400_BAD_REQUEST
            )

class InsuranceSearch(APIView):
    def get(self, request):
        queryset = Insurance.objects.all()
        search = request.query_params.get('q', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(phone_number__icontains=search)
            )
        serializer = InsuranceSerializer(queryset, many=True)
        return Response(serializer.data)