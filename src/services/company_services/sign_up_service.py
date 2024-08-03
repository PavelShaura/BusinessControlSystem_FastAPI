from fastapi import BackgroundTasks, HTTPException

from src.utils.mail_utils.send_email_service import EmailService
from src.utils.mail_utils.invite_mail_token_utils import (
    generate_invite_token,
    save_invite_token,
)
from src.schemas.company_schemas import SignUpResponse


class SignUpService:
    @staticmethod
    async def sign_up(uow, background_tasks: BackgroundTasks, email):
        try:
            async with uow:
                existing_user = await uow.user_repository.get_by_email(email)
                if existing_user:
                    raise ValueError("Email already registered")

                invite_token = generate_invite_token()
                save_invite_token(email, invite_token)
                email_service = EmailService()
                background_tasks.add_task(
                    email_service.send_invite_email, email, invite_token
                )

                return SignUpResponse(
                    message="Verification email sent", email=email
                ).model_dump()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
