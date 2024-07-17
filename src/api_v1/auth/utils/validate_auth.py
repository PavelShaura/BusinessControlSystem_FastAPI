from fastapi import Form, HTTPException, status, Depends

from src.api_v1.auth.utils.password_utils import validate_password
from src.utils.unit_of_work import UnitOfWork, get_uow


async def validate_auth_user(
    email: str = Form(), password: str = Form(), uow: UnitOfWork = Depends(get_uow)
):
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

        if not user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user inactive",
            )

    return user
