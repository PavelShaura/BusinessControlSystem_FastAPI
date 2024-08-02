from sqlalchemy import text

from src.schemas.task_schemas import UserInfo, TaskResponse


class TaskServiceHelper:
    @staticmethod
    async def get_task_details(uow, task):
        try:
            author = await uow.user_repository.get_by_id(task.author_id)
            responsible = (
                await uow.user_repository.get_by_id(task.responsible_id)
                if task.responsible_id
                else None
            )

            watchers = await uow.session.execute(
                text("SELECT user_id FROM task_watchers WHERE task_id = :task_id"),
                {"task_id": task.id},
            )
            watcher_ids = [row[0] for row in watchers]

            executors = await uow.session.execute(
                text("SELECT user_id FROM task_executors WHERE task_id = :task_id"),
                {"task_id": task.id},
            )
            executor_ids = [row[0] for row in executors]

            watcher_users = [
                await uow.user_repository.get_by_id(watcher_id)
                for watcher_id in watcher_ids
            ]
            executor_users = [
                await uow.user_repository.get_by_id(executor_id)
                for executor_id in executor_ids
            ]

            task_dict = task.__dict__.copy()
            task_dict["author"] = UserInfo.model_validate(author.__dict__)
            task_dict["responsible"] = (
                UserInfo.model_validate(responsible.__dict__) if responsible else None
            )
            task_dict["watchers"] = [
                UserInfo.model_validate(watcher.__dict__)
                for watcher in watcher_users
                if watcher
            ]
            task_dict["executors"] = [
                UserInfo.model_validate(executor.__dict__)
                for executor in executor_users
                if executor
            ]

            return TaskResponse.model_validate(task_dict)
        except ValueError as e:
            raise ValueError(f"Error getting task details: {str(e)}")
