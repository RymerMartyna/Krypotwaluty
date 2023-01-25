from datetime import datetime

# import pandas as pd
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
# print(cg.ping()) #confirm connection

coins_list = cg.get_coins_list()

# Get list of available choices
def get_names():
    return [x["name"] for x in coins_list]


# Get price of the chosen coin in the chosen currency
def get_price(coins, currencies):
    return cg.get_price(ids=coins, vs_currencies=currencies)


# Glowna funkcja -> zwraca cene bitcoina w wybranej walucie i date z godzina
def bitcoins_current_price(currency):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return {
        "price": get_price("bitcoin", currency)["bitcoin"][currency],
        "datetime": dt_string,
    }


print(bitcoins_current_price("eur"))
