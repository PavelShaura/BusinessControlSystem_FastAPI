from fastapi import HTTPException

from src.utils.logging_logic import logger
from src.utils.mail_utils.invite_mail_token_utils import verify_invite_token
from src.schemas.company_schemas import MessageResponse


class VerifySignUpService:
    @staticmethod
    async def verify_sign_up(email, invite_token):
        try:
            if not verify_invite_token(email, invite_token):
                logger.info(f"Invalid or expired invite token to email {email}")
                raise ValueError("Invalid or expired invite token")

            return MessageResponse(message="Email verified successfully").model_dump()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
