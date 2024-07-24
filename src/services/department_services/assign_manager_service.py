from src.services.base_service import BaseService
from src.schemas.department_schemas import DepartmentResponse


class AssignManagerService(BaseService):
    async def execute(self, uow, department_id: int, manager_id: int):
        async with uow:
            department = await uow.department_repository.get_by_id(department_id)
            if not department:
                raise ValueError("Department not found")

            manager = await uow.user_repository.get_by_id(manager_id)
            if not manager:
                raise ValueError("Manager not found")

            department.manager_id = manager_id
            await uow.department_repository.update(department)
            await uow.commit()

            return DepartmentResponse.model_validate(department)
