from fastapi import APIRouter, Depends, Form

from src.schemas.auth_schemas import TokenInfo
from src.services.auth_services.sign_in_service import SignInService
from src.utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter(tags=["sign-in"])


@router.post("/api/v1/auth/sign-in", response_model=TokenInfo)
async def sign_in_on_app(
    email: str = Form(), password: str = Form(), uow: UnitOfWork = Depends(get_uow)
):
    return await SignInService()(uow, email=email, password=password)
