from fastapi import HTTPException

from src.schemas.position_schemas import PositionResponse


class CreatePositionService:
    try:

        @staticmethod
        async def create_position(uow, name, company_id):
            async with uow:
                new_position = await uow.position_repository.create(
                    name=name, company_id=company_id
                )
                await uow.commit()

            return PositionResponse.model_validate(new_position)

    except ValueError as e:
        raise HTTPException(400, detail=f"Failed to create position: {str(e)}")
