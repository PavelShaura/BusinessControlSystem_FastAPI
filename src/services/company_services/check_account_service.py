from fastapi import HTTPException

from src.schemas.company_schemas import MessageResponse


class CheckAccountService:
    @staticmethod
    async def check_account(uow, email):
        try:
            async with uow:
                user = await uow.user_repository.get_by_email(email)
                if user:
                    raise ValueError("Email already registered")
                return MessageResponse(message="Email is available")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
