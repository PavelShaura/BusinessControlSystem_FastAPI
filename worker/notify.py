import asyncio

from celery.utils.log import get_task_logger

from src.utils.mail_utils.send_email_service import EmailService
from worker.tasks import celery_app


logger = get_task_logger(__name__)


@celery_app.task(name='send_invite_email')
def send_invite_email_task(email: str, invite_token: str):
    logger.info(f"Sending invite email to {email} with token {invite_token}")
    email_service = EmailService()
    asyncio.run(email_service.send_invite_email(email, invite_token))
    logger.info(f"Invite email sent to {email}")
    # Запуск:
    # celery -A worker.tasks:celery_app worker --loglevel=info
