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
    position_data: PositionCreate,
    uow: UnitOfWork = Depends(get_uow),
    create_position_service: position_services.CreatePositionService = Depends(
        position_services.CreatePositionService
    ),
):
    return await create_position_service.create_position(
        uow, position_data.name, position_data.company_id
    )


@router.put("/api/v1/positions/{position_id}", response_model=PositionResponse)
async def update_position(
    position_id: int,
    position_data: PositionUpdate,
    uow: UnitOfWork = Depends(get_uow),
    update_position_service: position_services.UpdatePositionService = Depends(
        position_services.UpdatePositionService
    ),
):
    return await update_position_service.update_position(
        uow, position_id, position_data.name, position_data.company_id
    )


@router.delete("/api/v1/positions/{position_id}")
async def delete_position(
    position_id: int,
    uow: UnitOfWork = Depends(get_uow),
    delete_position_service: position_services.DeletePositionService = Depends(
        position_services.DeletePositionService
    ),
):
    return await delete_position_service.delete_position(uow, position_id)
