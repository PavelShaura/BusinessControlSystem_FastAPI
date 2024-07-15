from fastapi import Form, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import InvalidTokenError

from src.auth.utils.jwt_utils import decode_jwt
from src.auth.utils.password_utils import validate_password
from src.user.models import User
from src.user.repository import UserRepository
from src.core.database import get_async_session


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login",
)


async def get_user_repository(session: AsyncSession = Depends(get_async_session)):
    return UserRepository(session)


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    user_repo: UserRepository = Depends(get_user_repository),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user = await user_repo.get_by_username(username)
    if not user:
        raise unauthed_exc

    if not validate_password(
        password=password,
        hashed_password=user.hashed_password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    username: str | None = payload.get("sub")
    user = await user_repo.get_by_username(username)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


async def get_current_active_auth_user(
    user: User = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )
