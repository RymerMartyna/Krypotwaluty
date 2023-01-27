from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime

class CryptoPrice(models.Model):
    cryptocurrency = models.CharField("cryptocurrency", max_length=240, db_column='cryptocurrency')
    price = models.FloatField(db_column="price")
    date_of_price = models.DateTimeField(db_column="date_of_price")

    def __str__(self):
        return self.cryptocurrency
    
    class Meta:
        db_table = "price_history"

class Email(models.Model):
    email = models.CharField("email", max_length=240, db_column='email')
    cryptocurrency = models.CharField("cryptocurrency", max_length=240, db_column='cryptocurrency')
    created_on = models.DateTimeField(db_column="created_on", default=datetime.now())

    def __str__(self):
        return self.email

    class Meta:
        db_table = "emails"

class Prediction(models.Model):
    cryptocurrency = models.CharField("cryptocurrency", max_length=255, db_column='cryptocurrency')
    date_of_prediction = models.CharField("date_of_prediction", db_column='date_of_prediction')
    prediction = models.CharField("prediction", max_length=255, db_column='prediction')
    def __str__(self):
        return self.prediction

    class Meta:
        db_table = "predictions"
    
    
    
    