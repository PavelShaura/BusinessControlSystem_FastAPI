from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from src.auth.utils.get_current_user_info import (
    get_current_token_payload,
    get_current_auth_user,
    get_current_active_auth_user,
)

from src.user.repository import get_user_repository
from src.core.database import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


async def auth_middleware(request: Request, call_next):
    public_paths = ["/login/", "/register/", "/docs", "/redoc", "/openapi.json"]

    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    try:
        token = await oauth2_scheme(request)
        payload = get_current_token_payload(token)

        async for session in get_async_session():
            user_repo = await get_user_repository(session)
            user = await get_current_auth_user(payload, user_repo)
            active_user = await get_current_active_auth_user(user)

        request.state.user = active_user
        request.state.token_payload = payload

    except HTTPException as http_exc:
        return JSONResponse(
            status_code=http_exc.status_code, content={"detail": http_exc.detail}
        )
    except Exception as e:
        return JSONResponse(status_code=401, content={"detail": str(e)})

    return await call_next(request)
