from fastapi import APIRouter, Depends

from src.api.v1.department.utils.show_department_hierarchy import (
    show_department_hierarchy,
)
from src.schemas.department_schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    AssignManager,
)
from src.services import department_services
from src.utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter(tags=["departments"])


@router.patch(
    "/api/v1/departments/{department_id}/assign_manager",
    response_model=DepartmentResponse,
)
async def assign_manager(
    department_id: int,
    assign_data: AssignManager,
    uow: UnitOfWork = Depends(get_uow),
    assign_manager_service: department_services.AssignManagerService = Depends(
        department_services.AssignManagerService
    ),
):
    return await assign_manager_service.assign(
        uow, department_id, assign_data.manager_id
    )


@router.post("/api/v1/departments", response_model=DepartmentResponse)
async def create_department(
    department_data: DepartmentCreate,
    uow: UnitOfWork = Depends(get_uow),
    create_department_services: department_services.CreateDepartmentService = Depends(
        department_services.CreateDepartmentService
    ),
):
    return await create_department_services.create_department(uow, department_data)


@router.put("/api/v1/departments/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    uow: UnitOfWork = Depends(get_uow),
    update_department_service: department_services.UpdateDepartmentService = Depends(
        department_services.UpdateDepartmentService
    ),
):

    return await update_department_service.update_department(
        uow, department_id, department_data
    )


@router.delete("/api/v1/departments/{department_id}")
async def delete_department(
    department_id: int,
    uow: UnitOfWork = Depends(get_uow),
    delete_department_service: department_services.DeleteDepartmentService = Depends(
        department_services.DeleteDepartmentService
    ),
):
    return await delete_department_service.delete_department(uow, department_id)


@router.get("/api/v1/departments/hierarchy")
async def get_department_hierarchy(uow: UnitOfWork = Depends(get_uow)):
    await show_department_hierarchy(uow)
    return {"message": "Department hierarchy printed to console"}
