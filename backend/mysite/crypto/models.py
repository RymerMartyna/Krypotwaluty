from django.db import models

# Create your models here.
from django.db import models

class CryptoPrice(models.Model):
    cryptocurrency = models.CharField("cryptoName", max_length=240, db_column='cryptocurrency')
    price = models.DecimalField(db_column="price", max_digits=999, decimal_places=10)
    date_of_price = models.DateTimeField(db_column="date_of_price")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "price_history"