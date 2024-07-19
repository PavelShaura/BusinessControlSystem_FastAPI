from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import EmailStr

from src.schemas.company_schemas import (
    InviteResponse,
    SignUpComplete,
    SignUpRequest,
)
from src.services import company_services
from src.utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter(tags=["sign-up"])


@router.post("/api/v1/auth/sign-up")
async def sign_up(
    sign_up_data: SignUpRequest,
    background_tasks: BackgroundTasks,
    uow: UnitOfWork = Depends(get_uow),
):
    return await company_services.SignUpService().execute(
        uow, background_tasks, email=sign_up_data.email, password=sign_up_data.password
    )


@router.post("/api/v1/auth/sign-up-verify")
async def verify_sign_up(
    account: str, invite_token: str, uow: UnitOfWork = Depends(get_uow)
):
    return await company_services.VerifySignUpService()(uow, account=account, invite_token=invite_token)


@router.post("/api/v1/auth/sign-up-complete")
async def complete_sign_up(
    user_data: SignUpComplete, uow: UnitOfWork = Depends(get_uow)
):
    return await company_services.CompleteSignUpService()(uow, user_data=user_data)


@router.get("/api/v1/check_account/{account}", response_model=InviteResponse)
async def check_account(account: EmailStr, uow: UnitOfWork = Depends(get_uow)):
    return await company_services.CheckAccountService()(uow, account=account)
