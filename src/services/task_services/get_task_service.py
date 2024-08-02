from fastapi import HTTPException

from src.services.task_services.utils.task_service_helper import TaskServiceHelper


class GetTaskService:
    @staticmethod
    async def get_task(uow, task_id):
        try:
            async with uow:
                task = await uow.task_repository.get_by_id(task_id)
                if not task:
                    raise HTTPException(status_code=404, detail="Task not found")

                return await TaskServiceHelper.get_task_details(uow, task)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
