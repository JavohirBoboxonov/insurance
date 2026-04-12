from django.urls import path
from insurance.views import InsuranceSearch, InsuranceCreate, InsuranceUpdate, InsuranceDelete

urlpatterns = [
    path('create/', InsuranceCreate.as_view(), name='insurance_create'),
    path('update/<int:id>/', InsuranceUpdate.as_view(), name='insurance_update'),
    path('search/', InsuranceSearch.as_view(), name='insurance_search'),
    path('delete/<int:id>/', InsuranceDelete.as_view(), name='insurance_delete'),
]