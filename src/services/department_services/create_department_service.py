from src.services.base_service import BaseService
from src.schemas.department_schemas import DepartmentCreate, DepartmentResponse


class CreateDepartmentService(BaseService):
    async def execute(self, uow, **kwargs):
        department_data = DepartmentCreate(**kwargs)

        async with uow:
            parent = None
            if department_data.parent_id:
                parent = await uow.department_repository.get_by_id(
                    department_data.parent_id
                )
                if not parent:
                    raise ValueError("Parent department not found")

            new_department = await uow.department_repository.create(
                name=department_data.name,
                company_id=department_data.company_id,
                parent=parent,
            )
            await uow.commit()

        return DepartmentResponse.model_validate(new_department)
