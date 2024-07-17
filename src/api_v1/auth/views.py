from fastapi import APIRouter, Depends
from datetime import datetime, timezone

from src.api_v1.auth.schemas import TokenInfo
from src.api_v1.auth.utils.jwt_utils import encode_jwt
from src.api_v1.auth.utils.validate_auth import validate_auth_user
from src.api_v1.user.schemas import UserSchema

router = APIRouter(tags=["sign-in"])


@router.post("/api/v1/auth/sign-in", response_model=TokenInfo)
async def sign_in(user: UserSchema = Depends(validate_auth_user)):
    current_time = datetime.now(timezone.utc)
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email,
        "is_admin": user.is_admin,
        "company_id": str(user.company_id),
        "iat": int(current_time.timestamp()),
    }
    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
