from fastapi import HTTPException

from src.services.base_service import BaseService
from src.schemas.department_schemas import DepartmentResponse, ManagerInfo


class AssignManagerService(BaseService):
    try:

        async def execute(self, uow, department_id: int, manager_id: int):
            async with uow:
                department = await uow.department_repository.get_by_id(department_id)
                if not department:
                    raise ValueError("Department not found")

                manager = await uow.user_repository.get_by_id(manager_id)
                if not manager:
                    raise ValueError("Manager not found")

                if manager.company_id != department.company_id:
                    raise ValueError(
                        "Manager and department must belong to the same company"
                    )

                await uow.department_repository.assign_manager(
                    department_id, manager_id
                )
                await uow.commit()

                manager_info = ManagerInfo(
                    manager_id=manager.id,
                    manager_name=f"{manager.first_name} {manager.last_name}",
                )
                department_response = DepartmentResponse(
                    id=department.id,
                    name=department.name,
                    company_id=department.company_id,
                    manager_info=manager_info,
                )
            return department_response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
