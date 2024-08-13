import asyncio

from celery.utils.log import get_task_logger

from src.utils.mail_utils.send_email_service import EmailService
from worker.celery import celery_app


logger = get_task_logger(__name__)


@celery_app.task(name="send_invite_email")
def send_invite_email_task(email: str, invite_token: str):
    logger.info(f"Sending invite email to {email} with token {invite_token}")
    email_service = EmailService()
    asyncio.run(email_service.send_invite_email(email, invite_token))
    logger.info(f"Invite email sent to {email}")


@celery_app.task(name="send_rebind_email")
def send_rebind_email_task(email: str, rebind_url: str):
    logger.info(f"Sending rebind email to {email} with URL {rebind_url}")
    email_service = EmailService()
    asyncio.run(email_service.send_rebind_email(email, rebind_url))
    logger.info(f"Rebind email sent to {email}")


@celery_app.task(name="send_employee_invite_email")
def send_employee_invite_email_task(email: str, invite_url: str):
    logger.info(f"Sending invite email to {email} with URL {invite_url}")
    email_service = EmailService()
    asyncio.run(email_service.send_initial_invite_email(email, invite_url))
    logger.info(f"Invite email sent to {email}")

# Запуск:
# celery -A worker.tasks:celery_app worker --loglevel=info
