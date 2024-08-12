from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import EmailStr

from src.schemas.company_schemas import (
    MessageResponse,
    SignUpRequest,
    CompleteSignUpRequest,
    VerifySignUpRequest,
)
from src.services import company_services
from src.utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter(tags=["sign-up"])


@router.post("/api/v1/auth/sign-up")
async def sign_up(
    sign_up_data: SignUpRequest,
    uow: UnitOfWork = Depends(get_uow),
    sign_up_service: company_services.SignUpService = Depends(
        company_services.SignUpService
    ),
):
    return await sign_up_service.sign_up(uow, sign_up_data.email)


@router.post("/api/v1/auth/sign-up-verify")
async def verify_sign_up(
    verify_data: VerifySignUpRequest,
    verify_sign_up_service: company_services.VerifySignUpService = Depends(
        company_services.VerifySignUpService
    ),
):
    return await verify_sign_up_service.verify_sign_up(
        verify_data.email, verify_data.invite_token
    )


@router.post("/api/v1/auth/sign-up-complete")
async def complete_sign_up(
    user_data: CompleteSignUpRequest,
    uow: UnitOfWork = Depends(get_uow),
    complete_sign_up_service: company_services.CompleteSignUpService = Depends(
        company_services.CompleteSignUpService
    ),
):
    return await complete_sign_up_service.comlete_sign_up(uow, user_data)


@router.get("/api/v1/check_account/{account}", response_model=MessageResponse)
async def check_account(
    account: EmailStr,
    uow: UnitOfWork = Depends(get_uow),
    check_account_service: company_services.CheckAccountService = Depends(
        company_services.CheckAccountService
    ),
):
    return await check_account_service.check_account(uow, account)
