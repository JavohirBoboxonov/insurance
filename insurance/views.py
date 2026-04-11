from rest_framework.views import APIView
from serializer import *
from django.db.models import Q
from models import Insurance
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class InsuranceCreate(APIView):
    def post(self, request):
        serializer = InsuranceCreate(data=request.data)
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
        

class InsuranceSearch(viewsets.ModelViewSet):
    serializer_class = InsuranceSerializer

    def get_queryset(self):
        queryset = Insurance.objects.all()
        search = self.request.query_params.get('q', None)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search),
                Q(phone_number__icontains=search)
            )
        return queryset