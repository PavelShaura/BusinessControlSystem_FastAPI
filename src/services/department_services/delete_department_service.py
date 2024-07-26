from fastapi import HTTPException

from src.services.base_service import BaseService
from src.schemas.department_schemas import DepartmentMessageResponse


class DeleteDepartmentService(BaseService):
    try:

        async def execute(self, uow, department_id: int):
            async with uow:
                department = await uow.department_repository.get_by_id(department_id)
                if not department:
                    raise ValueError("Department not found")

                await uow.department_repository.delete(department_id)
                await uow.commit()

            return DepartmentMessageResponse(message="Department deleted successfully")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
