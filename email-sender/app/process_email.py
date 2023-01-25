from celery import Celery
import os

user = os.environ["RABBITMQ_USER"]
password = os.environ["RABBITMQ_PASS"]

CELERY_BROKER_URL=f"amqp://{user}:{password}@rabbitmq:5672/"

# user = 'user'
# password = 'password'
#
# CELERY_BROKER_URL=f"amqp://{user}:{password}@localhost:5672/"

app = Celery('email', broker=CELERY_BROKER_URL)

@app.task
def process_email(email, crypto, price, currency):
    print(f" {email} {crypto} {price} {currency}")