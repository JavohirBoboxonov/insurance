from rest_framework import viewsets
from serializer import *
from django.db.models import Q
from models import Insurance
# Create your views here.

class InsuranceViewSet(viewsets.ModelViewSet):
    queryset = Insurance.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return InsuranceCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return InsuranceUpdateSerializer
        

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