from django.urls import include, path
from .views import CryptoPriceList

urlpatterns = [
    path('test/', CryptoPriceList.as_view()),
]