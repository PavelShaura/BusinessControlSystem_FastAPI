from fastapi import HTTPException

from src.schemas.company_schemas import MessageResponse
from src.utils.logging_logic import logger


class CheckAccountService:
    @staticmethod
    async def check_account(uow, email):
        try:
            async with uow:
                user = await uow.user_repository.get_by_email(email)
                if user:
                    logger.info(f"Email {email} already registered")
                    raise ValueError("Email already registered")
                return MessageResponse(message="Email is available")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
