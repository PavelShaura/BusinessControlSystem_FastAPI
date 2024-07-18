from src.api.v1.company.utils.email_utils import send_invite_email
from src.api.v1.company.utils.invite_utils import generate_invite_token, save_invite_token
from src.services.base_service import BaseService


class SignUpService(BaseService):
    async def execute(self, uow, **kwargs):
        email = kwargs.get('email')
        async with uow:
            existing_user = await uow.user_repository.get_by_email(email)
            if existing_user:
                raise ValueError("Email already registered")

            invite_token = generate_invite_token()
            save_invite_token(email, invite_token)

            await send_invite_email(email, invite_token)

            return {"message": "Verification email sent", "email": email}