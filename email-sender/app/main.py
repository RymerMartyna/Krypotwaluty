from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@rabbitmq//')

@app.task
def add(x, y):
    return x + y