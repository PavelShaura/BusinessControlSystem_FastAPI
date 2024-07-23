from src.services.base_service import BaseService
from src.schemas.position_schemas import PositionUpdate, PositionResponse


class UpdatePositionService(BaseService):
    async def execute(self, uow, position_id: int, **kwargs):
        position_data = PositionUpdate(**kwargs)

        async with uow:
            position = await uow.position_repository.get_by_id(position_id)
            if not position:
                raise ValueError("Position not found")

            await uow.position_repository.update(
                position_id, **position_data.dict(exclude_unset=True)
            )
            await uow.commit()

            updated_position = await uow.position_repository.get_by_id(position_id)

        return PositionResponse.from_orm(updated_position)
