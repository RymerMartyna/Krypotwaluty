from celery import Celery
import os
import smtplib, ssl
import time

# user = "user"
# password = "password"

# CELERY_BROKER_URL=f"amqp://{user}:{password}@localhost:5672/"

user = 'user'
password = 'password'

CELERY_BROKER_URL = f"amqp://{user}:{password}@rabbitmq:5672/"

app = Celery('email', broker=CELERY_BROKER_URL)

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "aplikacjakryptowalutytest@gmail.com"
password = "llfjfuahshnqjmvo"


def setup_smpt():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login(sender_email, password)
    print("email")
    return s


def close_server(s):
    s.quit()


@app.task
def process_email(email, crypto, price, currency):
    s = setup_smpt()

    def send_email():
        # s = get_server()
        message = f"""\
    Subject: Hi there

    Hello {email}. Price for {crypto} is {price} {currency}"""
        s.sendmail(sender_email, email, message)

    send_email()
    # close_server(s)
