import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(
    sender: str, recipient: str | None, text: str, gmail_app_password: str
) -> None:
    if recipient is None:
        # assumes the sender is the admin of 'seasontracker'
        send_email(
            sender, sender, "ERROR: missing recipient for email.", gmail_app_password
        )
        sys.exit(1)

    if text == "":
        # no need to send the email
        return

    msg = MIMEMultipart()
    msg["Subject"] = "Notification from seasontracker"
    msg["From"] = sender
    msg["To"] = recipient

    msg.attach(MIMEText(text))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        _ = smtp.login(sender, gmail_app_password)
        _ = smtp.send_message(msg)

    return
