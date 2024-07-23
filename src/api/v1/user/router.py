from fastapi import APIRouter, Depends, HTTPException

from src.schemas.user_schemas import UserUpdate
from src.services.user_services.update_user_service import UpdateUserService
from src.utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter(tags=["users"])


@router.patch("/api/v1/users/{user_id}", response_model=UserUpdate)
async def update_user(
    user_id: int, update_data: UserUpdate, uow: UnitOfWork = Depends(get_uow)
):
    try:
        user = await UpdateUserService().execute(uow, user_id, update_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
