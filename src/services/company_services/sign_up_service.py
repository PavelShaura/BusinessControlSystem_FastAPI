from fastapi import HTTPException

from src.utils.logging_logic import logger
from src.utils.mail_utils.invite_mail_token_utils import (
    generate_invite_token,
    save_invite_token,
)
from src.schemas.company_schemas import SignUpResponse
from src.utils.rabbitmq_utils.rabbitmq_producer import RabbitMQProducer


class SignUpService:
    @staticmethod
    async def sign_up(uow, email):
        try:
            async with uow:
                existing_user = await uow.user_repository.get_by_email(email)
                if existing_user:
                    logger.info(f"Email {email} already registered")
                    raise ValueError("Email already registered")

                invite_token = generate_invite_token()
                save_invite_token(email, invite_token)

                # Используем RabbitMQ для отправки задачи
                rabbitmq_producer = RabbitMQProducer()
                await rabbitmq_producer.connect()
                await rabbitmq_producer.publish(
                    'email_tasks',
                    {'task': 'send_invite_email', 'args': [email, invite_token]}
                )
                await rabbitmq_producer.close()

            return SignUpResponse(
                message="Verification email sent", email=email
            ).model_dump()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
