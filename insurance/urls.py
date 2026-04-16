from django.urls import path
from insurance.views import InsuranceSearch, InsuranceCreate, InsuranceUpdate, InsuranceDelete, InsuranceDetail

urlpatterns = [
    path('create/', InsuranceCreate.as_view(), name='insurance_create'),
    path('update/<int:id>/', InsuranceUpdate.as_view(), name='insurance_update'),
    path('search/', InsuranceSearch.as_view(), name='insurance_search'),
    path('delete/<int:id>/', InsuranceDelete.as_view(), name='insurance_delete'),
    path('detail/<int:pk/>', InsuranceDetail.as_view(), name='insurance_detail'),
]