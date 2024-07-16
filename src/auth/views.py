from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import TokenInfo
from src.auth.utils.validate_auth import validate_auth_user
from src.auth.utils.jwt_utils import encode_jwt
from src.auth.utils.password_utils import hash_password
from src.core.database import get_async_session
from src.user.repository import UserRepository
from src.user.schemas import UserSchema, CreateUser, UserResponse, UserInfo

router = APIRouter(tags=["JWT"])


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    current_time = datetime.now(timezone.utc)
    jwt_payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
        "iat": int(current_time.timestamp()),
    }
    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/users/{username}", response_model=UserInfo)
async def auth_user_check_self_info(
    username: str,
    request: Request,
):
    user = request.state.user
    payload = request.state.token_payload
    if user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this user's information",
        )
    logged_in_at = datetime.fromtimestamp(payload.get("iat", 0), timezone.utc)
    return UserInfo(username=user.username, email=user.email, logged_in_at=logged_in_at)


@router.post("/register/", response_model=UserResponse)
async def register_user(
    user_data: CreateUser,
    session: AsyncSession = Depends(get_async_session),
):
    user_repo = UserRepository(session)

    if await user_repo.get_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    if await user_repo.get_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)

    new_user = await user_repo.add_one_and_get_obj(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        active=True,
    )

    await session.commit()

    return UserResponse(username=new_user.username, email=new_user.email)
