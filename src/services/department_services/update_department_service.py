from fastapi import HTTPException

from src.schemas.department_schemas import DepartmentResponse, DepartmentUpdate


class UpdateDepartmentService:
    @staticmethod
    async def update_department(
        uow, department_id: int, department_data: DepartmentUpdate
    ):
        try:
            async with uow:
                updated_department = await uow.department_repository.update(
                    department_id,
                    name=department_data.name,
                    parent_id=department_data.parent,
                )
                await uow.commit()
                return DepartmentResponse.model_validate(updated_department)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
