from django.urls import path
from .views import *
urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('telegram_login/', TelegramLogin.as_view(), name='telegram_login'),
    path('logout/', SignOut.as_view(), name='signout'),
    path('verify/', VerifyApi.as_view(), name='varify')
]