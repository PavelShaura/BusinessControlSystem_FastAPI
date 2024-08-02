from fastapi import HTTPException

from src.schemas.base_schemas import MessageResponse


class DeleteTaskService:
    @staticmethod
    async def delete_task(uow, task_id):
        try:
            async with uow:
                task = await uow.task_repository.get_by_id(task_id)
                if not task:
                    raise HTTPException(status_code=404, detail="Task not found")

                await uow.task_repository.delete(task_id)
                await uow.commit()

                return MessageResponse(message="Task successfully deleted")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
