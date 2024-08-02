from datetime import datetime

from sqlalchemy import select

from src.utils.repository import SqlAlchemyRepository
from src.models.task_models import Task, TaskWatcher, TaskExecutor


class TaskRepository(SqlAlchemyRepository):
    model = Task

    async def get_by_id(self, task_id: int):
        query = select(self.model).where(self.model.id == task_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, **kwargs):
        if "deadline" in kwargs:
            deadline = kwargs["deadline"]
            if deadline and isinstance(deadline, datetime) and deadline.tzinfo:
                kwargs["deadline"] = deadline.replace(tzinfo=None)

        watchers = kwargs.pop("watchers", [])
        executors = kwargs.pop("executors", [])
        task = await self.add_one_and_get_obj(**kwargs)

        for watcher in watchers:
            self.session.add(TaskWatcher(task_id=task.id, user_id=watcher.id))
        for executor in executors:
            self.session.add(TaskExecutor(task_id=task.id, user_id=executor.id))

        await self.session.flush()
        return task

    async def update(self, task_id: int, **kwargs):
        if "deadline" in kwargs:
            deadline = kwargs["deadline"]
            if deadline and isinstance(deadline, datetime) and deadline.tzinfo:
                kwargs["deadline"] = deadline.replace(tzinfo=None)

        watchers = kwargs.pop("watchers", None)
        executors = kwargs.pop("executors", None)

        task = await self.update_one_by_id(task_id, **kwargs)

        if watchers is not None:
            await self.session.execute(
                TaskWatcher.__table__.delete().where(TaskWatcher.task_id == task_id)
            )
            for watcher_id in watchers:
                self.session.add(TaskWatcher(task_id=task_id, user_id=watcher_id))

        if executors is not None:
            await self.session.execute(
                TaskExecutor.__table__.delete().where(TaskExecutor.task_id == task_id)
            )
            for executor_id in executors:
                self.session.add(TaskExecutor(task_id=task_id, user_id=executor_id))

        await self.session.flush()
        return task

    async def delete(self, task_id: int):
        await self.session.execute(
            TaskWatcher.__table__.delete().where(TaskWatcher.task_id == task_id)
        )
        await self.session.execute(
            TaskExecutor.__table__.delete().where(TaskExecutor.task_id == task_id)
        )
        await self.delete_by_query(id=task_id)
