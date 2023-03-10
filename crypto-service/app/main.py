# import pandas as pd
# import plotly.graph_objects as go
# from plotly.ofline import plot
import os
from datetime import datetime

import psycopg2
from celery import Celery
from pycoingecko import CoinGeckoAPI

user = os.environ["RABBITMQ_USER"]
password = os.environ["RABBITMQ_PASS"]
CELERY_BROKER_URL = f"amqp://{user}:{password}@rabbitmq:5672/"

pg_user = os.environ["POSTGRES_USER"]
pg_password = os.environ["POSTGRES_PASSWORD"]
pg_database = os.environ["POSTGRES_DATABASE"]
pg_host = "postgres"
# user = 'user'
# password = 'password'
# CELERY_BROKER_URL=f"amqp://{user}:{password}@localhost:5672/"

app = Celery("crypto", broker=CELERY_BROKER_URL)
cg = CoinGeckoAPI()
coins_list = ["bitcoin"]

currency = "usd"
conn = psycopg2.connect(
    database="default", user=pg_user, password=pg_password, host=pg_host, port="5432"
)
days = 2



def initial_load():
    print("Executing initial load")
    cur = conn.cursor()
    sql = f"TRUNCATE table price_history"
    print(f"executing {sql}")
    cur.execute(sql)
    print("executed")
    conn.commit()
    for coin in coins_list:
        history = cg.get_coin_market_chart_by_id(coin, vs_currency=currency, days=2)["prices"]

        output = []
        for entry in history:
            date = datetime.fromtimestamp(entry[0]/1000.0)
            output.append({"date_time": date, "price": entry[1]})

            cur = conn.cursor()
            sql = f"INSERT INTO price_history (cryptocurrency, price, date_of_price) VALUES ('{coin}', {entry[1]}, '{date}')"
            print(f"executing {sql}")
            cur.execute(sql)
            print("executed")
            conn.commit()

        process_crypto()
        make_prediction(conn, coin)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, process_crypto.s(), name='process crypto after 60 seconds')
    initial_load()

@app.task
def process_crypto():
    prices = get_price(coins_list, currency)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    for crypto in coins_list:
        price = prices[crypto][currency]
        ## save crypto to db
        write_price_to_db(crypto, price)
        make_prediction(conn, crypto)
        ## send emails
        emails = select_from_db(crypto)
        for email in emails:
            app.send_task(
                "process_email.process_email",
                args=[email, crypto, price, currency],
                queue="email_queue",
            )


# # Get list of available choices
# def get_names():
#     return [x["name"] for x in coins_list]


def write_price_to_db(currency, price):
    print("write price to db")
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO price_history (cryptocurrency, price, date_of_price) "
        f"VALUES ('{currency}', {price}, current_timestamp)"
    )
    conn.commit()


# Get price of the chosen coin in the chosen currency
def get_price(coins, currencies):
    return cg.get_price(ids=coins, vs_currencies=currencies, precision="full")


def select_from_db(cryptocurrency):
    email_list = []
    try:
        cursor = conn.cursor()
        postgreSQL_select_Query = (
            f"select * from emails where cryptocurrency='{cryptocurrency}'"
        )

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


def select_historical_prices_from_db(cryptocurrency):
    historical_list = []
    try:
        cursor = conn.cursor()
        postgreSQL_select_Query = (
            f"SELECT * from price_history where cryptocurrency='{cryptocurrency}'"
        )

        cursor.execute(postgreSQL_select_Query)
        # print("Selecting rows from price_history table using cursor.fetchall")
        historical_records = cursor.fetchall()

        for row in historical_records:
            historical_list.append(row[1])

        return historical_list

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()

from prophet import Prophet
import pandas.io.sql as psql


def empty_table(connection):
    cur = connection.cursor()
    sql = f"truncate table predictions"
    print(f"executing {sql}")
    cur.execute(sql)
    print("executed")
    connection.commit()


def insert_predictions(connection, forecast, coin):
    cur = connection.cursor()
    for index, row in forecast.iterrows():
        sql = f"INSERT INTO predictions (date_of_prediction, prediction, cryptocurrency) VALUES ('{row['ds']}', " \
              f"{row['yhat']}, '{coin}')"
        print(f"executing {sql}")
        cur.execute(sql)

    connection.commit()


def make_prediction(connection, coin):
    df = psql.read_sql("select * from price_history", connection)
    df = df.rename(columns={"price": "y", "date_of_price": "ds"})

    # Creating forecast
    pr = Prophet()
    pr.fit(df)
    future = pr.make_future_dataframe(periods=7)
    forecast = pr.predict(future)

    forecast = forecast[["ds", "yhat"]]

    empty_table(connection)
    insert_predictions(connection, forecast, coin)
