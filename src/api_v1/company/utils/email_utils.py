from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

from src.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)


async def send_invite_email(email: EmailStr, invite_token: str):
    html = f"""
    <html>
        <body>
            <h1>Welcome to Our Platform!</h1>
            <p>Благодарим за регистрацию вашей компании! Для подтверждения введите код на странице:</p>
            <h2>{invite_token}</h2>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="BusinessControlSystem_app",
        recipients=[email],
        body=html,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
