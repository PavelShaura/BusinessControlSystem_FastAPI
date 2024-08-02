from fastapi import HTTPException

from src.schemas.position_schemas import PositionResponse


class UpdatePositionService:
    @staticmethod
    async def update_position(uow, position_id, name, company_id):
        try:
            async with uow:
                position = await uow.position_repository.get_by_id(position_id)
                if not position:
                    raise ValueError("Position not found")
                await uow.position_repository.update(
                    position_id, name=name, company_id=company_id
                )
                await uow.commit()
                updated_position = await uow.position_repository.get_by_id(position_id)
            return PositionResponse.model_validate(updated_position)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
