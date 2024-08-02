from fastapi import HTTPException

from src.models.task_models import TaskWatcher, TaskExecutor
from src.services.task_services.utils.task_service_helper import TaskServiceHelper


class UpdateTaskService:
    @staticmethod
    async def update_task(uow, task_id: int, task_data):
        try:
            async with uow:
                task = await uow.task_repository.get_by_id(task_id)
                if not task:
                    raise HTTPException(status_code=404, detail="Task not found")

                update_data = task_data.dict(exclude_unset=True)

                if "responsible_id" in update_data:
                    responsible = await uow.user_repository.get_by_id(
                        update_data["responsible_id"]
                    )
                    if not responsible:
                        raise HTTPException(
                            status_code=404, detail="Responsible user not found"
                        )

                updated_task = await uow.task_repository.update(task_id, **update_data)

                if "watchers" in update_data:
                    await uow.session.execute(
                        TaskWatcher.__table__.delete().where(
                            TaskWatcher.task_id == task_id
                        )
                    )
                    for watcher_id in update_data["watchers"]:
                        watcher = await uow.user_repository.get_by_id(watcher_id)
                        if watcher:
                            uow.session.add(
                                TaskWatcher(task_id=task_id, user_id=watcher_id)
                            )

                if "executors" in update_data:
                    await uow.session.execute(
                        TaskExecutor.__table__.delete().where(
                            TaskExecutor.task_id == task_id
                        )
                    )
                    for executor_id in update_data["executors"]:
                        executor = await uow.user_repository.get_by_id(executor_id)
                        if executor:
                            uow.session.add(
                                TaskExecutor(task_id=task_id, user_id=executor_id)
                            )

                await uow.commit()

                updated_task = await uow.task_repository.get_by_id(task_id)
                return await TaskServiceHelper.get_task_details(uow, updated_task)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
