from typing import List
from app.configs.config import settings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


class SMTPService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.mail_username,
            MAIL_PASSWORD=settings.mail_password,
            MAIL_FROM=settings.mail_from,
            MAIL_PORT=settings.mail_port,
            MAIL_SERVER=settings.mail_server,
            MAIL_FROM_NAME=settings.mail_from_name,
            MAIL_TLS=True,
            MAIL_SSL=False,
            USE_CREDENTIALS=True,
            TEMPLATE_FOLDER='./templates/email'
        )
    async def send_email_async(self, subject: str, email_to_list: List[str], body: dict):
        message = MessageSchema(
            subject=subject,
            recipients=email_to_list,
            body=body,
            subtype='html'
        )

        fm = FastMail(self.conf)
        await fm.send_message(message=message, template_name='email.html')
