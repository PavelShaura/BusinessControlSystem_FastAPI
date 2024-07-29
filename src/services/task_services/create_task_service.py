from fastapi import HTTPException

from src.schemas.task_schemas import TaskCreate, TaskResponse, UserInfo
from src.services.base_service import BaseService
from src.models.task_models import TaskWatcher, TaskExecutor


class CreateTaskService(BaseService):
    try:

        async def execute(self, uow, request, task_data: TaskCreate):
            user_id = int(request.state.user_id)
            async with uow:
                author = await uow.user_repository.get_by_id(user_id)
                if not author:
                    raise HTTPException(status_code=404, detail="Author not found")

                responsible = None
                if task_data.responsible_id:
                    responsible = await uow.user_repository.get_by_id(
                        task_data.responsible_id
                    )
                    if not responsible:
                        raise HTTPException(
                            status_code=404, detail="Responsible user not found"
                        )

                new_task = await uow.task_repository.create(
                    title=task_data.title,
                    description=task_data.description,
                    author_id=user_id,
                    responsible_id=task_data.responsible_id,
                    deadline=task_data.deadline,
                    estimated_time=task_data.estimated_time,
                )

                for watcher_id in task_data.watchers:
                    watcher = await uow.user_repository.get_by_id(watcher_id)
                    if watcher:
                        uow.session.add(
                            TaskWatcher(task_id=new_task.id, user_id=watcher_id)
                        )

                for executor_id in task_data.executors:
                    executor = await uow.user_repository.get_by_id(executor_id)
                    if executor:
                        uow.session.add(
                            TaskExecutor(task_id=new_task.id, user_id=executor_id)
                        )

                await uow.commit()

                new_task_dict = new_task.__dict__.copy()
                new_task_dict["author"] = UserInfo.model_validate(author.__dict__)
                new_task_dict["responsible"] = (
                    UserInfo.model_validate(responsible.__dict__)
                    if responsible
                    else None
                )

                new_task_dict["watchers"] = [
                    UserInfo.model_validate(
                        (await uow.user_repository.get_by_id(watcher_id)).__dict__
                    )
                    for watcher_id in task_data.watchers
                ]

                new_task_dict["executors"] = [
                    UserInfo.model_validate(
                        (await uow.user_repository.get_by_id(executor_id)).__dict__
                    )
                    for executor_id in task_data.executors
                ]

                return TaskResponse.model_validate(new_task_dict)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
