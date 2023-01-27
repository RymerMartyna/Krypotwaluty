from django.urls import include, path
from .views import CryptoPriceList, EmailRegister, PredictionList, index

urlpatterns = [
    path('price/', CryptoPriceList.as_view()),
    path('email/', EmailRegister.as_view()),
    path('prediction/', PredictionList.as_view()),
    path("", index, name="index")
]