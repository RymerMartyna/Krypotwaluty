from rest_framework import serializers
from .models import CryptoPrice

class CryptoPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CryptoPrice 
        fields = ['cryptocurrency', 'price', 'date_of_price']
