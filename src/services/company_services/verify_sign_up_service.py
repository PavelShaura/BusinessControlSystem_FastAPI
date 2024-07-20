from src.api.v1.company.utils.invite_utils import verify_invite_token
from src.services.base_service import BaseService
from src.schemas.company_schemas import VerifySignUpRequest, MessageResponse


class VerifySignUpService(BaseService):
    async def execute(self, uow, **kwargs):
        verify_sign_up_request = VerifySignUpRequest(**kwargs)
        email = verify_sign_up_request.email
        invite_token = verify_sign_up_request.invite_token

        if not verify_invite_token(email, invite_token):
            raise ValueError("Invalid or expired invite token")

        return MessageResponse(message="Email verified successfully").model_dump()
