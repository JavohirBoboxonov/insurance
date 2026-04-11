from rest_framework.views import APIView
from serializer import *
from django.db.models import Q
from models import Insurance
from rest_framework import viewsets
# Create your views here.

class InsuranceCreate(APIView):
    def post(self, request):
        serializer = InsuranceCreate(data=request.data)
        if serializer.is_valid():
            serializer.save()
        
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