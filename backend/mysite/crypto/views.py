from django.shortcuts import render
# Czy nie powinno tu być tez from models import Email, Prediction?
from .models import CryptoPrice, Prediction
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializer import CryptoPriceSerializer, EmailSerializer, PredictionSerializer
import datetime

def index(request):
    return render(request, "index.html")

class CryptoPriceList(generics.ListAPIView):
    # API endpoint that allows customer to be viewed.
    
    serializer_class = CryptoPriceSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            minutes = int(self.request.GET.get('minutes', "3"))
            print(minutes)
            # queryset = CryptoPrice.objects.all()
            queryset = CryptoPrice.objects.filter(date_of_price__gte=datetime.datetime.now() - datetime.timedelta(minutes=minutes))
            return queryset
        else:
            return 0

class EmailRegister(generics.ListAPIView):
    # API endpoint that allows customer to be viewed.

    serializer_class = EmailSerializer

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'email': request.data.get('email'),
            'cryptocurrency': request.data.get('cryptocurrency')
        }
        serializer = EmailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PredictionList(generics.ListAPIView):
    # API endpoint that allows customer to be viewed.
    
    serializer_class = PredictionSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            minutes = int(self.request.GET.get('minutes', "3"))
            print(minutes)
      
            queryset = Prediction.objects.filter(date_of_prediction__gte=datetime.datetime.now() - datetime.timedelta(minutes=minutes))
            return queryset
        else:
            return 0