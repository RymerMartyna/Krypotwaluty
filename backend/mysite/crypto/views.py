from django.shortcuts import render
from .models import CryptoPrice
from rest_framework import generics
from .serializer import CryptoPriceSerializer
import datetime

class CryptoPriceList(generics.ListAPIView):
    # API endpoint that allows customer to be viewed.
    
    serializer_class = CryptoPriceSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            minutes = int(self.request.GET.get('minutes', "60"))
            print(minutes)
            queryset = CryptoPrice.objects.filter(date_of_price__lte=datetime.datetime.now() - datetime.timedelta(minutes=minutes))
            return queryset