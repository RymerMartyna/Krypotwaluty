from celery import Celery
import os

user = os.environ["RABBITMQ_USER"]
password = os.environ["RABBITMQ_PASS"]

CELERY_BROKER_URL=f"amqp://{user}:{password}@rabbitmq:5672/"

app = Celery('tasks', broker=CELERY_BROKER_URL)

@app.task
def add(x, y):
    return x + y