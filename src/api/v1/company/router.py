from fastapi import APIRouter, Depends
from pydantic import EmailStr

from src.schemas.company_schemas import (
    InviteResponse,
    SignUpComplete,
    SignUpRequest,
)
from src.services.company_services.check_account_service import CheckAccountService
from src.services.company_services.complete_sign_up_service import CompleteSignUpService
from src.services.company_services.sign_up_service import SignUpService
from src.services.company_services.verify_sign_up_service import VerifySignUpService
from src.utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter(tags=["sign-up"])


@router.post("/api/v1/auth/sign-up")
async def sign_up(sign_up_data: SignUpRequest, uow: UnitOfWork = Depends(get_uow)):
    return await SignUpService()(
        uow, email=sign_up_data.email, password=sign_up_data.password
    )


@router.post("/api/v1/auth/sign-up-verify")
async def verify_sign_up(
    account: str, invite_token: str, uow: UnitOfWork = Depends(get_uow)
):
    return await VerifySignUpService()(uow, account=account, invite_token=invite_token)


@router.post("/api/v1/auth/sign-up-complete")
async def complete_sign_up(
    user_data: SignUpComplete, uow: UnitOfWork = Depends(get_uow)
):
    return await CompleteSignUpService()(uow, user_data=user_data)


@router.get("/api/v1/check_account/{account}", response_model=InviteResponse)
async def check_account(account: EmailStr, uow: UnitOfWork = Depends(get_uow)):
    return await CheckAccountService()(uow, account=account)
