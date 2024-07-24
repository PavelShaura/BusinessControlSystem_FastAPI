from fastapi import APIRouter, Depends, HTTPException

from src.schemas.department_schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    AssignManager,
)
from src.services import department_services
from src.services.department_services import AssignManagerService
from src.utils.unit_of_work import UnitOfWork, get_uow

router = APIRouter(tags=["departments"])


@router.patch(
    "/api/v1/departments/{department_id}/assign_manager",
    response_model=DepartmentResponse,
)
async def assign_manager(
    department_id: int, assign_data: AssignManager, uow: UnitOfWork = Depends(get_uow)
):
    try:
        department = await AssignManagerService().execute(
            uow, department_id, assign_data.manager_id
        )
        return department
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/v1/departments", response_model=DepartmentResponse)
async def create_department(
    department_data: DepartmentCreate, uow: UnitOfWork = Depends(get_uow)
):
    try:
        return await department_services.CreateDepartmentService()(
            uow, **department_data.dict()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/api/v1/departments/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    uow: UnitOfWork = Depends(get_uow),
):
    try:
        return await department_services.UpdateDepartmentService()(
            uow, department_id, **department_data.dict(exclude_unset=True)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/api/v1/departments/{department_id}")
async def delete_department(department_id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        return await department_services.DeleteDepartmentService()(uow, department_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
