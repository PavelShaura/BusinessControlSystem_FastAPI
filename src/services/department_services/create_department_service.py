from fastapi import HTTPException

from src.services.base_service import BaseService
from src.schemas.department_schemas import DepartmentCreate, DepartmentResponse


class CreateDepartmentService(BaseService):
    try:

        async def execute(self, uow, **kwargs) -> DepartmentResponse:
            department_data = DepartmentCreate(**kwargs)
            async with uow:
                new_department = await uow.department_repository.create(
                    name=department_data.name,
                    company_id=department_data.company_id,
                    parent_id=department_data.parent_id,
                )
                await uow.commit()
            return DepartmentResponse.model_validate(new_department)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
