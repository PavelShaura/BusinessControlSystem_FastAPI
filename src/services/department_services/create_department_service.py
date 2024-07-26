from fastapi import HTTPException

from src.services.base_service import BaseService
from src.schemas.department_schemas import DepartmentCreate, DepartmentResponse


class CreateDepartmentService(BaseService):
    try:

        async def execute(self, uow, **kwargs):
            department_data = DepartmentCreate(**kwargs)

            async with uow:
                new_department = await uow.department_repository.create(
                    **department_data.model_dump()
                )
                await uow.commit()

            return DepartmentResponse.model_validate(new_department)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
