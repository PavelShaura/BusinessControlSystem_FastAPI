from src.schemas.position_schemas import PositionMessageResponse
from src.services.base_service import BaseService


class DeletePositionService(BaseService):
    async def execute(self, uow, position_id: int):
        async with uow:
            position = await uow.position_repository.get_by_id(position_id)
            if not position:
                raise ValueError("Position not found")

            await uow.position_repository.delete(position_id)
            await uow.commit()

        return PositionMessageResponse(message="Position deleted successfully")
