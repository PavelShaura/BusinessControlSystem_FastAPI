from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from src.api.v1.auth.utils.jwt_utils import decode_jwt
from src.api.v1.user.repository import UserRepository
from src.utils.unit_of_work import get_uow

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/sign-in")


async def auth_middleware(request: Request, call_next):
    public_paths = [
        "/api/v1/auth/sign-in",
        "/api/v1/auth/sign-up",
        "/api/v1/auth/sign-up-verify",
        "/api/v1/auth/sign-up-complete",
        "/api/v1/employees/registration-complete",
        "/api/v1/check_account/",
        "/api/v1/employees/confirm-rebind-email",
        "/docs",
        "/redoc",
        "/openapi.json",
    ]

    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    try:
        token = await oauth2_scheme(request)
        payload = decode_jwt(token)

        user_id = payload.get("sub")
        email = payload.get("email")
        is_admin = payload.get("is_admin")
        company_id = payload.get("company_id")

        if not all([user_id, email, company_id]):
            raise HTTPException(status_code=401, detail="Invalid token payload")

        async for uow in get_uow():
            user_repo = UserRepository(uow.session)
            user = await user_repo.get_by_id(int(user_id))

            if not user or user.email != email or str(user.company_id) != company_id:
                raise HTTPException(
                    status_code=401, detail="User not found or invalid token data"
                )

            if not user.is_active:
                raise HTTPException(status_code=403, detail="User inactive")
            request.state.user_id = user_id
            request.state.user = user
            request.state.is_admin = is_admin
            request.state.company_id = company_id
            break

    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"detail": http_exc.detail}
        )

    return await call_next(request)
