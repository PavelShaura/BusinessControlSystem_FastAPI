from src.services.base_service import BaseService
from src.schemas.department_schemas import DepartmentUpdate, DepartmentResponse


class UpdateDepartmentService(BaseService):
    async def execute(self, uow, department_id: int, **kwargs):
        department_data = DepartmentUpdate(**kwargs)

        async with uow:
            department = await uow.department_repository.get_by_id(department_id)
            if not department:
                raise ValueError("Department not found")

            await uow.department_repository.update(
                department_id, **department_data.dict(exclude_unset=True)
            )
            await uow.commit()

            updated_department = await uow.department_repository.get_by_id(
                department_id
            )

        return DepartmentResponse.model_validate(updated_department)
