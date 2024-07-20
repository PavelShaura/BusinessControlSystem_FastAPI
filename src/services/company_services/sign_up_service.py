from fastapi import BackgroundTasks

from src.api.v1.company.utils.email_utils import send_invite_email
from src.api.v1.company.utils.invite_utils import (
    generate_invite_token,
    save_invite_token,
)
from src.services.base_service import BaseService
from src.schemas.company_schemas import SignUpRequest, SignUpResponse


class SignUpService(BaseService):
    async def execute(self, uow, background_tasks: BackgroundTasks, **kwargs):
        sign_up_request = SignUpRequest(**kwargs)
        email = sign_up_request.email
        async with uow:
            existing_user = await uow.user_repository.get_by_email(email)
            if existing_user:
                raise ValueError("Email already registered")

            invite_token = generate_invite_token()
            save_invite_token(email, invite_token)

            # Добавление задачи для отправки письма в фоне
            background_tasks.add_task(send_invite_email, email, invite_token)

            return SignUpResponse(
                message="Verification email sent", email=email
            ).model_dump()
