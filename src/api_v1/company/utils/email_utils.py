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
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_invite_email(email: EmailStr, invite_token: str):
    html = f"""
    <html>
        <body>
            <h1>Welcome to Our Platform!</h1>
            <p>You have been invited to join. Please use the following token to complete your registration:</p>
            <h2>{invite_token}</h2>
            <p>This token will expire in 24 hours.</p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Invitation to Join Our Platform",
        recipients=[email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)