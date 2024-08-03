from datetime import datetime, timezone

from fastapi import HTTPException, status

from src.api.v1.auth.utils.jwt_utils import encode_jwt
from src.api.v1.auth.utils.password_utils import validate_password
from src.schemas.auth_schemas import TokenInfo
from src.utils.logging_logic import logger


class SignInService:
    async def sign_in(self, uow, email, password) -> TokenInfo:
        try:
            user = await self._validate_auth_user(email, password, uow)

            current_time = datetime.now(timezone.utc)
            jwt_payload = {
                "sub": str(user.id),
                "email": user.email,
                "is_admin": user.is_admin,
                "company_id": str(user.company_id),
                "iat": int(current_time.timestamp()),
            }
            token = encode_jwt(jwt_payload)
            return TokenInfo(access_token=token, token_type="Bearer")
        except Exception as e:
            logger.info(f"An error: {e} occurred while logging in to email: {email}")

    async def _validate_auth_user(self, email: str, password: str, uow):
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid email or password",
        )

        async with uow:
            user = await uow.user_repository.get_by_email(email)
            if not user:
                raise unauthed_exc

            if not validate_password(
                password=password,
                hashed_password=user.hashed_password,
            ):
                raise unauthed_exc

            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="user inactive",
                )

        return user
