from fastapi import APIRouter, Depends, Form

from src.schemas.auth_schemas import TokenInfo, SignInRequest
from src.services.auth_services.sign_in_service import SignInService
from src.utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter(tags=["sign-in"])


@router.post("/api/v1/auth/sign-in", response_model=TokenInfo)
async def sign_in(
    sign_in_request: SignInRequest,
    uow: UnitOfWork = Depends(get_uow),
    sign_in_service: SignInService = Depends(SignInService),
):
    return await sign_in_service.sign_in(
        uow, sign_in_request.email, sign_in_request.password
    )
