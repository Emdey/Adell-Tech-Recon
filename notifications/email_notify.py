import smtplib
from email.message import EmailMessage
from config import EMAIL_FROM, EMAIL_TO, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_NOTIFICATIONS

def send_email(subject: str, body: str):
    if not EMAIL_NOTIFICATIONS:
        return
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"[+] Email sent: {subject}")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")
