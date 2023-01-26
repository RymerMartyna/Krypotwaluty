# Import smtplib for the actual sending function
import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "aplikacjakryptowalutytest@gmail.com"
receiver_email = "luthien.shadow@gmail.com"
password = "ogveyhrbpebkxwhz"


message = """\
Subject: Hi there

This message is sent from Python."""


# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
