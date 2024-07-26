from fastapi import APIRouter, Depends

from src.schemas.position_schemas import (
    PositionCreate,
    PositionUpdate,
    PositionResponse,
)
from src.services import position_services
from src.utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter(tags=["positions"])


@router.post("/api/v1/positions", response_model=PositionResponse)
async def create_position(
    position_data: PositionCreate, uow: UnitOfWork = Depends(get_uow)
):
    return await position_services.CreatePositionService()(
            uow, **position_data.model_dump()
        )



@router.put("/api/v1/positions/{position_id}", response_model=PositionResponse)
async def update_position(
    position_id: int, position_data: PositionUpdate, uow: UnitOfWork = Depends(get_uow)
):
    return await position_services.UpdatePositionService()(
            uow, position_id, **position_data.dict(exclude_unset=True)
        )


@router.delete("/api/v1/positions/{position_id}")
async def delete_position(position_id: int, uow: UnitOfWork = Depends(get_uow)):
    return await position_services.DeletePositionService()(uow, position_id)

