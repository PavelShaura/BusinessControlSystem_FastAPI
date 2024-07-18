from src.api.v1.company.utils.invite_utils import verify_invite_token
from src.services.base_service import BaseService


class VerifySignUpService(BaseService):
    async def execute(self, uow, **kwargs):
        account = kwargs.get("account")
        invite_token = kwargs.get("invite_token")
        if not verify_invite_token(account, invite_token):
            raise ValueError("Invalid or expired invite token")
        return {"message": "Email verified successfully"}
