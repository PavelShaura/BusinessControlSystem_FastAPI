from src.services.base_service import BaseService
from src.schemas.position_schemas import PositionCreate, PositionResponse


class CreatePositionService(BaseService):
    async def execute(self, uow, **kwargs):
        position_data = PositionCreate(**kwargs)

        async with uow:
            new_position = await uow.position_repository.create(
                name=position_data.name, company_id=position_data.company_id
            )
            await uow.commit()

        return PositionResponse.model_validate(new_position)
