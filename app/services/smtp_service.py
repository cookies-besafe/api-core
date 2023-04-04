from typing import List
from app.configs.config import settings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


class SMTPService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.mail_username,
            MAIL_PASSWORD=settings.mail_password,
            MAIL_FROM=settings.mail_from,
            MAIL_PORT=settings.mail_port,
            MAIL_SERVER=settings.mail_server,
            MAIL_FROM_NAME=settings.mail_from_name,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

    def get_html(self, body: dict):
        return f"""
            <html>
                <body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
                <div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
                <div style="margin: 0 auto; width: 90%; text-align: center;">
                    <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">{ body.get('name') } is in potential danger!</h1>
                    <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center;">
                    <h3 style="margin-bottom: 100px; font-size: 24px;">{ body.get('name') }!</h3>
                    <p style="margin-bottom: 30px;">{body.get('name')} sent SOS REQUEST, please check if everything is ok</p>
                    </div>
                </div>
                </div>
                </body>
            </html>
        """

    async def send_email_async(self, subject: str, email_to_list: List[str], body: dict):
        message = MessageSchema(
            subject=subject,
            recipients=email_to_list,
            body=self.get_html(body=body),
            subtype=MessageType.html
        )

        fm = FastMail(self.conf)
        await fm.send_message(message=message)
