from fastapi import HTTPException

from src.schemas.position_schemas import PositionMessageResponse


class DeletePositionService:
    @staticmethod
    async def delete_position(uow, position_id: int):
        try:
            async with uow:
                position = await uow.position_repository.get_by_id(position_id)
                if not position:
                    raise ValueError("Position not found")

                await uow.position_repository.delete(position_id)
                await uow.commit()

            return PositionMessageResponse(message="Position deleted successfully")
        except ValueError as e:
            raise HTTPException(400, detail=str(e))
