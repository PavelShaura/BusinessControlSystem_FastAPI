from fastapi import Form, HTTPException, status, Depends

from src.api_v1.auth.utils.password_utils import validate_password
from src.api_v1.user.repository import UserRepository, get_user_repository


async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
    user_repo: UserRepository = Depends(get_user_repository),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    user = await user_repo.get_by_email(email)
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
