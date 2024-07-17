from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import EmailStr

from src.api_v1.auth.utils.password_utils import hash_password
from src.api_v1.company.utils.email_utils import send_invite_email
from src.api_v1.company.utils.invite_utils import (
    generate_invite_token,
    save_invite_token,
    verify_invite_token,
)
from src.api_v1.company.schemas import (
    InviteResponse,
    EmployeeCreate,
    SignUpComplete,
    CompanyInfo,
)
from src.utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter(tags=["company"])


@router.get("api/v1/check_account/{account}")
async def check_account(account: EmailStr, uow: UnitOfWork = Depends(get_uow)):
    async with uow:
        user = await uow.user_repository.get_by_email(account)
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")

        invite_token = generate_invite_token()
        save_invite_token(account, invite_token)

        # Отправка email с инвайт-токеном
        await send_invite_email(account, invite_token)

    return {"message": "Invitation sent to email"}


@router.post("api/v1/auth/sign-up#verify", response_model=InviteResponse)
async def sign_up(account: str, invite_token: str):
    if not verify_invite_token(account, invite_token):
        raise HTTPException(status_code=400, detail="Invalid or expired invite token")
    return InviteResponse(message="Email verified successfully")


@router.post("api/v1/auth/sign-up#complete", response_model=EmployeeCreate)
async def sign_up_complete(
    user_data: SignUpComplete, uow: UnitOfWork = Depends(get_uow)
):
    async with uow:
        existing_user = await uow.user_repository.get_by_email(user_data.account)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        company = await uow.company_repository.get_by_name(user_data.company_name)
        if not company:
            company = await uow.company_repository.create(name=user_data.company_name)

        hashed_password = hash_password(user_data.password)
        new_user = await uow.user_repository.create(
            email=user_data.account,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            is_admin=True,
            company_id=company.id,
        )

        await uow.commit()

    return EmployeeCreate(
        email=new_user.email,
        password=hashed_password,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        company_name=company.name,
    )


@router.get("/api/v1/company/{username}", response_model=CompanyInfo)
async def get_company_info(
    username: str, request: Request, uow: UnitOfWork = Depends(get_uow)
):
    user = request.state.user
    if user.email != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this company's information",
        )

    async with uow:
        company = await uow.company_repository.get_by_id(user.company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found",
            )

        employees = await uow.user_repository.get_by_company_id(user.company_id)

    return CompanyInfo(
        name=company.name, admin_email=user.email, employee_count=len(employees)
    )
