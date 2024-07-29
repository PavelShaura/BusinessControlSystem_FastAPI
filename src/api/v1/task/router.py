from fastapi import APIRouter, Depends, Request

from src.utils.unit_of_work import UnitOfWork, get_uow
from src.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse
from src.schemas.base_schemas import MessageResponse
from src.services import task_services

router = APIRouter(tags=["tasks"])


@router.post("/api/v1/tasks", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate, request: Request, uow: UnitOfWork = Depends(get_uow)
):
    return await task_services.CreateTaskService().execute(
        uow, request=request, task_data=task_data
    )


@router.get("/api/v1/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, uow: UnitOfWork = Depends(get_uow)):
    return await task_services.GetTaskService().execute(uow, task_id=task_id)


@router.put("/api/v1/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int, task_data: TaskUpdate, uow: UnitOfWork = Depends(get_uow)
):
    return await task_services.UpdateTaskService().execute(
        uow, task_id=task_id, task_data=task_data
    )


@router.delete("/api/v1/tasks/{task_id}", response_model=MessageResponse)
async def delete_task(task_id: int, uow: UnitOfWork = Depends(get_uow)):
    return await task_services.DeleteTaskService().execute(uow, task_id=task_id)
