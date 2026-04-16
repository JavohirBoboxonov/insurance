from rest_framework.views import APIView
from .serializer import *
from django.db.models import Q
from .models import Insurance
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class InsuranceCreate(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = InsuranceCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response({
                "detail": "Ma`lumotlar noto`g`ri kiritilgan",
                "errors": serializer.errors
            }, status=400)

        insurance = serializer.save()

        return Response({
            "detail": "Sug`urta yaratildi",
            "data": InsuranceCreateSerializer(insurance).data,
        }, status=201)

class InsuranceDetail(APIView):
    def get(self, request, id):
        insurance_item = get_object_or_404(Insurance, id=id)
        if not insurance_item:
            return Response({
                "bu id dagi sug`urta yo`q"
            }, status=400)
        serializer = InsuranceSerializer(insurance_item)
        return Response({
            "data": serializer.data
        }, status=200)

class InsuranceUpdate(APIView):
    permission_classes = (IsAuthenticated, )

    serializer_class = InsuranceCreateSerializer

    def patch(self, request, id):
        try:
            insurance = Insurance.objects.get(id=id)
        except Insurance.DoesNotExist:
            return Response({
                "error": "Bunday id dagi sug`urta Topilmadi"
            },status=400)
        
        serializer = InsuranceCreateSerializer(
            insurance, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "detail": "Yangilandi",
                "data": serializer.data,
            }, status=200)
        return Response({
            "error": serializer.errors
        }, status=400)
        
class InsuranceDelete(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, id):
        try:
            insurance = Insurance.objects.get(id=id)
            insurance.delete()

            return Response({
                "message": "Sug'urta muvaffaqiyatli o'chirildi"
            }, status=status.HTTP_200_OK)

        except Insurance.DoesNotExist:
            return Response(
                {"error": "Bunday ID dagi sug'urta topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )

class InsuranceSearch(APIView):
    def get(self, request):
        queryset = Insurance.objects.all()
        search = request.query_params.get('q', None)
        if search:
            search = search.strip().replace(' ', '+')
            
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(phone_number__icontains=search)
            )
        serializer = InsuranceSerializer(queryset, many=True)
        return Response(serializer.data)