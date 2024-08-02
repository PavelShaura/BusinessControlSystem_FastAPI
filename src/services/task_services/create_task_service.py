from fastapi import HTTPException

from src.schemas.task_schemas import TaskResponse, UserInfo
from src.models.task_models import TaskWatcher, TaskExecutor


class CreateTaskService:
    @staticmethod
    async def create_task(uow, request, task_data):
        try:
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

                missing_watchers = []
                for watcher_id in task_data.watchers:
                    watcher = await uow.user_repository.get_by_id(watcher_id)
                    if watcher:
                        uow.session.add(
                            TaskWatcher(task_id=new_task.id, user_id=watcher_id)
                        )
                    else:
                        missing_watchers.append(watcher_id)

                missing_executors = []
                for executor_id in task_data.executors:
                    executor = await uow.user_repository.get_by_id(executor_id)
                    if executor:
                        uow.session.add(
                            TaskExecutor(task_id=new_task.id, user_id=executor_id)
                        )
                    else:
                        missing_executors.append(executor_id)

                await uow.commit()

                new_task_dict = new_task.__dict__.copy()
                new_task_dict["author"] = UserInfo.model_validate(author.__dict__)
                new_task_dict["responsible"] = (
                    UserInfo.model_validate(responsible.__dict__)
                    if responsible
                    else None
                )

                new_task_dict["watchers"] = [
                    UserInfo.model_validate(watcher.__dict__)
                    for watcher_id in task_data.watchers
                    if (watcher := await uow.user_repository.get_by_id(watcher_id))
                    is not None
                ]

                new_task_dict["executors"] = [
                    UserInfo.model_validate(executor.__dict__)
                    for executor_id in task_data.executors
                    if (executor := await uow.user_repository.get_by_id(executor_id))
                    is not None
                ]

                task_response = TaskResponse.model_validate(new_task_dict)

                if missing_watchers or missing_executors:
                    missing_users = []
                    if missing_watchers:
                        missing_users.append(f"Missing watchers: {missing_watchers}")
                    if missing_executors:
                        missing_users.append(f"Missing executors: {missing_executors}")
                    task_response.warning = "Some users do not exist: " + ", ".join(
                        missing_users
                    )

                return task_response

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
