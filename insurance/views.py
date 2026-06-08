from rest_framework.views import APIView
from .serializer import *
from django.db.models import Q
from .models import InsuranceWay
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiExample

class DynamicPagination(LimitOffsetPagination):
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    
    default_limit = 10

class InsuranceListView(ListAPIView):
    queryset = InsuranceWay.objects.all().select_related('id')
    serializer_class = InsuranceSerializer
    pagination_class = DynamicPagination

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
        insurance_item = get_object_or_404(InsuranceWay, id=id)
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

    @extend_schema(
        request=InsuranceDateUpdateSerializer,
        responses={200: InsuranceDateUpdateSerializer, 400: "Bad Request", 404: "Not Found"},
        description="Sug'urta muddatini qisman yangilash Api",
        examples=[
            OpenApiExample(
                name="Sana yangilash namunasi",
                value={
                    "expiry_date": "2026-12-31"
                },
                request_only=True,
            )
        ]
    )

    def patch(self, request, id):
        try:
            insurance = InsuranceWay.objects.get(id=id)
        except InsuranceWay.DoesNotExist:
            return Response({
                "error": "There is no insurance on such an ID."
            },status=404)
        
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
    
class InsuranceDateUpdate(APIView):
    permission_classes = (IsAuthenticated, )
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "expiry_date": {
                        "type": "string",
                        "format": "date",
                        "description": "Sug'urtaning yangi tugash sanasi (YYYY-MM-DD)",
                        "example": "2026-12-31"
                    }
                },
                "required": ["expiry_date"]
            }
        },
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Updated"},
                    "data": {
                        "type": "object",
                        "properties": {
                            "expiry_date": {"type": "string", "format": "date", "example": "2026-12-31"}
                        }
                    }
                }
            },
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT
        },
        description="Sug'urta muddatini yangilash uchun Api"
    )
    def patch(self, request, id):
        try:
            insurance = InsuranceWay.objects.get(id=id)
        except InsuranceWay.DoesNotExist:
            return Response({
                "error": "There is no insurance on such ID."
            }, status=404)
        
        serializer = InsuranceDateUpdateSerializer(
            insurance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "detail": "Updated",
                "data": serializer.data,
            })
        return Response({
            "error": serializer.errors
        }, status=400)

class InsuranceDelete(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, id):
        try:
            insurance = InsuranceWay.objects.get(id=id)
            insurance.delete()

            return Response({
                "message": "Insurance succesfully deleted"
            }, status=status.HTTP_200_OK)

        except InsuranceWay.DoesNotExist:
            return Response(
                {"error": "There is no insurance on such an ID."},
                status=status.HTTP_404_NOT_FOUND
            )

class InsuranceSearch(APIView):
    def get(self, request):
        queryset = InsuranceWay.objects.all()
        search = request.query_params.get('q', None)
        if search:
            search = search.strip()
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(phone_number__icontains=search)
            )
        serializer = InsuranceSerializer(queryset, many=True)
        return Response(serializer.data)