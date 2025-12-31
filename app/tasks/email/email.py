from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib

from app.core.config import settings


async def send_email(
    recipient: str,
    subject: str,
    plain_content: str,
    html_content: str = "",
):
    sender_email = settings.sender_email
    app_password = settings.app_password

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject

    plain_text_message = MIMEText(plain_content, "plain", "utf-8")
    message.attach(plain_text_message)

    if html_content:
        html_message = MIMEText(html_content, "html", "utf-8")
        message.attach(html_message)

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        username=sender_email,
        password=app_password,
        use_tls=True,
    )
