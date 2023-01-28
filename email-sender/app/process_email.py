from celery import Celery
import os
import smtplib

user = os.environ["RABBITMQ_USER"]
password = os.environ["RABBITMQ_PASS"]

CELERY_BROKER_URL = f"amqp://{user}:{password}@rabbitmq:5672/"

app = Celery('email', broker=CELERY_BROKER_URL)

sender_email = os.environ["GMAIL_SENDER_EMAIL"]
password = os.environ["GMAIL_SENDER_PASSWORD"]

port = 465  # For SSL
smtp_server = "smtp.gmail.com"

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
    Subject: Najnowszy kurs Twojej kryptowaluty {crypto}

    Cześć {email}. Obecna cena {crypto} wynosi {price} {currency}"""
        s.sendmail(sender_email, email, message)

    send_email()
    # close_server(s)
