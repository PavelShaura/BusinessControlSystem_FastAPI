from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

from src.core.config import settings


class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
        )
        self.fm = FastMail(self.conf)

    async def send_email(self, subject: str, email: EmailStr, html_content: str):
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            body=html_content,
            subtype="html",
        )
        await self.fm.send_message(message)

    async def send_invite_email(self, email: EmailStr, invite_url: str):
        html = f"""
        <html>
            <body>
                <h1>Welcome to Our Platform!</h1>
                <p>Благодарим за регистрацию вашей компании! Для завершения регистрации введите токен:</p>
                <p>{invite_url}</p>
            </body>
        </html>
        """
        await self.send_email("BusinessControlSystem_app - Registration", email, html)

    async def send_rebind_email(self, email: EmailStr, rebind_url: str):
        html = f"""
        <html>
            <body>
                <h1>Rebind Email Address</h1>
                <p>Для подтверждения привязки новой почты, пожалуйста, перейдите по следующей ссылке:</p>
                <a href="{rebind_url}">Confirm new email</a>
            </body>
        </html>
        """
        await self.send_email("BusinessControlSystem_app - Rebind Email", email, html)

    async def send_initial_invite_email(self, email: EmailStr, invite_url: str):
        html = f"""
        <html>
            <body>
                <h1>Welcome to Our Company!</h1>
                <p>Вы были приглашены присоединиться к нашей компании. Для завершения регистрации, пожалуйста, перейдите по следующей ссылке:</p>
                <a href="{invite_url}">Complete Registration</a>
            </body>
        </html>
        """
        await self.send_email("BusinessControlSystem_app - Invitation", email, html)


def get_email_service():
    return EmailService()