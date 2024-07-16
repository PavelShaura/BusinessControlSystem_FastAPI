from fastapi import HTTPException, status
from jwt import InvalidTokenError

from src.api_v1.auth.utils.jwt_utils import decode_jwt
from src.api_v1.user.models import User
from src.api_v1.user.repository import UserRepository


def get_current_token_payload(token: str) -> dict:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error",
        )
    return payload


async def get_current_auth_user(payload: dict, user_repo: UserRepository) -> User:
    username: str | None = payload.get("username")
    user = await user_repo.get_by_username(username)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


async def get_current_active_auth_user(user: User):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )
