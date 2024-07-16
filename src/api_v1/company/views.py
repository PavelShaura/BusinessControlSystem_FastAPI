from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.utils.password_utils import hash_password
from src.api_v1.company.utils.email_utils import send_invite_email
from src.api_v1.company.utils.invite_utils import generate_invite_token, save_invite_token, verify_invite_token
from src.api_v1.company.repository import CompanyRepository
from src.api_v1.company.schemas import InviteResponse, EmployeeCreate, SignUpComplete
from src.api_v1.user.repository import UserRepository
from src.core.database import get_async_session


router = APIRouter(tags=["company"])


@router.get("/check_account/{account}")
async def check_account(
        account: EmailStr,
        session: AsyncSession = Depends(get_async_session)
):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_email(account)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    invite_token = generate_invite_token()
    save_invite_token(account, invite_token)

    # Отправка email с инвайт-токеном
    await send_invite_email(account, invite_token)

    return {"message": "Invitation sent to email"}


@router.post("/sign-up", response_model=InviteResponse)
async def sign_up(
        account: str,
        invite_token: str,
        session: AsyncSession = Depends(get_async_session)
):
    if not verify_invite_token(account, invite_token):
        raise HTTPException(status_code=400, detail="Invalid or expired invite token")
    return {"message": "Email verified successfully"}


@router.post("/sign-up-complete", response_model=EmployeeCreate)
async def sign_up_complete(
        user_data: SignUpComplete,
        session: AsyncSession = Depends(get_async_session)
):
    user_repo = UserRepository(session)
    company_repo = CompanyRepository(session)

    existing_user = await user_repo.get_by_email(user_data.account)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    company = await company_repo.get_by_name(user_data.company_name)
    if not company:
        company = await company_repo.create(name=user_data.company_name)

    hashed_password = hash_password(user_data.password)
    new_user = await user_repo.create(
        email=user_data.account,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        is_admin=True,
        company_id=company.id
    )

    await session.commit()

    return EmployeeCreate(
        email=new_user.email,
        password=hashed_password,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        company_name=company.name
    )