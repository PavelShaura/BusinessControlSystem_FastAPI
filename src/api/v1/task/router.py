from fastapi import APIRouter, Depends, Request

from src.utils.unit_of_work import UnitOfWork, get_uow
from src.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse
from src.schemas.base_schemas import MessageResponse
from src.services import task_services

router = APIRouter(tags=["tasks"])


@router.post("/api/v1/tasks", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    request: Request,
    uow: UnitOfWork = Depends(get_uow),
    create_task_service: task_services.CreateTaskService = Depends(
        task_services.CreateTaskService
    ),
):
    return await create_task_service.create_task(uow, request, task_data)


@router.get("/api/v1/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    uow: UnitOfWork = Depends(get_uow),
    get_task_service: task_services.GetTaskService = Depends(
        task_services.GetTaskService
    ),
):
    return await get_task_service.get_task(uow, task_id)


@router.put("/api/v1/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    uow: UnitOfWork = Depends(get_uow),
    update_task_service: task_services.UpdateTaskService = Depends(
        task_services.UpdateTaskService
    ),
):
    return await update_task_service.update_task(uow, task_id, task_data)


@router.delete("/api/v1/tasks/{task_id}", response_model=MessageResponse)
async def delete_task(
    task_id: int,
    uow: UnitOfWork = Depends(get_uow),
    delete_task_service: task_services.DeleteTaskService = Depends(
        task_services.DeleteTaskService
    ),
):
    return await delete_task_service.delete_task(uow, task_id)
