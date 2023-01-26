# import pandas as pd
# import plotly.graph_objects as go
# from plotly.ofline import plot
import os
from pycoingecko import CoinGeckoAPI
from celery import Celery
from datetime import datetime
import psycopg2

user = os.environ["RABBITMQ_USER"]
password = os.environ["RABBITMQ_PASS"]
CELERY_BROKER_URL=f"amqp://{user}:{password}@rabbitmq:5672/"

pg_user = os.environ["POSTGRES_USER"]
pg_password = os.environ["POSTGRES_PASSWORD"]
pg_database = os.environ["POSTGRES_DATABASE"]
pg_host = "postgres"
# user = 'user'
# password = 'password'
# CELERY_BROKER_URL=f"amqp://{user}:{password}@localhost:5672/"

app = Celery('crypto', broker=CELERY_BROKER_URL)
cg = CoinGeckoAPI()
coins_list = ['bitcoin']

currency = 'usd'

conn = psycopg2.connect(database = "default", user = pg_user, password = pg_password,
                        host = pg_host, port = "5432")

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, process_crypto.s(), name='process crypto after 60 seconds')

@app.task
def process_crypto():
    prices = get_price(coins_list, currency)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    for crypto in coins_list:
        price = prices[crypto][currency]
        ## save crypto to db
        write_price_to_db(crypto, price)
        ## send emails
        emails = select_from_db(crypto)
        for email in emails:
            app.send_task("process_email.process_email", args=[email, crypto, price, currency], queue='email_queue')

# # Get list of available choices
# def get_names():
#     return [x["name"] for x in coins_list]

def write_price_to_db(currency, price):
    print("write price to db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO price_history (cryptocurrency, price, date_of_price) "
                f"VALUES ('{currency}', {price}, current_timestamp)")
    conn.commit()

# Get price of the chosen coin in the chosen currency
def get_price(coins, currencies):
    return cg.get_price(ids=coins, vs_currencies=currencies, precision="full")

def select_from_db(cryptocurrency):
    email_list = []
    try:
        cursor = conn.cursor()
        postgreSQL_select_Query = f"select * from emails where cryptocurrency='{cryptocurrency}'"

        cursor.execute(postgreSQL_select_Query)
        # print("Selecting rows from email table using cursor.fetchall")
        email_records = cursor.fetchall()

        for row in email_records:
            email_list.append(row[1])
            
        return email_list

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()