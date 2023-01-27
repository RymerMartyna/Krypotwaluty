from rest_framework import serializers
from .models import CryptoPrice, Email, Prediction

class CryptoPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CryptoPrice 
        fields = ['cryptocurrency', 'price', 'date_of_price']

class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = ['email', 'cryptocurrency', 'created_on']
        
class PredictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prediction
        fields = ['cryptocurrency', 'date_of_prediction', 'prediction']