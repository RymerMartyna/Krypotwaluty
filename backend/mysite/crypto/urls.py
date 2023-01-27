from django.urls import include, path
from .views import CryptoPriceList, EmailRegister

urlpatterns = [
    path('price/', CryptoPriceList.as_view()),
    path('email/', EmailRegister.as_view()),
]