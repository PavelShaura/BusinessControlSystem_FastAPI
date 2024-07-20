from src.schemas.company_schemas import MessageResponse
from src.services.base_service import BaseService


class CheckAccountService(BaseService):
    async def execute(self, uow, **kwargs):
        account = kwargs.get("account")
        async with uow:
            user = await uow.user_repository.get_by_email(account)
            if user:
                raise ValueError("Email already registered")
            return MessageResponse(message="Email is available")
