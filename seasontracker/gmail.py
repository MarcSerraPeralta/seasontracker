import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_test_email(email: str, gmail_app_password: str) -> None:
    msg = MIMEMultipart()
    msg["Subject"] = "Test email from seasontracker!"
    msg["From"] = email
    msg["To"] = email

    msg.attach(MIMEText("You will see here the new seasons from your shows."))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        _ = smtp.login(email, gmail_app_password)
        _ = smtp.send_message(msg)

    return
