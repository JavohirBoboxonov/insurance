from rest_framework.views import APIView
from .serializer import *
from django.db.models import Q
from .models import Insurance
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Insurance


class InsuranceListView(ListAPIView):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer

class InsuranceCreate(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = InsuranceCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response({
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
                "error": "There is no insurance on such an ID."
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
                "error": "There is no insurance on such an ID."
            },status=400)
        
        serializer = InsuranceCreateSerializer(
            insurance, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "detail": "Updated",
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
                "message": "Insurance succesfully deleted"
            }, status=status.HTTP_200_OK)

        except Insurance.DoesNotExist:
            return Response(
                {"error": "There is no insurance on such an ID."},
                status=status.HTTP_404_NOT_FOUND
            )

class InsuranceSearch(APIView):
    def get(self, request):
        queryset = Insurance.objects.all()
        search = request.query_params.get('q', None)
        if search:
            search = search.strip()
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(phone_number__icontains=search)
            )
        serializer = InsuranceSerializer(queryset, many=True)
        return Response(serializer.data)