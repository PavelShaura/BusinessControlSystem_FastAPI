from abc import ABC, abstractmethod
from typing import Type, Dict, Any, Optional

from celery.result import AsyncResult


class Task(ABC):
    """Базовый абстрактный класс для всех задач"""

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Optional[AsyncResult]:
        pass


class TaskFactory:
    """Фабрика задач с декоратором для регистрации"""

    _task_map: Dict[str, Type[Task]] = {}

    @classmethod
    def register(cls, task_type: str):
        def decorator(task_class: Type[Task]):
            cls._task_map[task_type] = task_class
            return task_class

        return decorator

    @classmethod
    def create_task(cls, task_type: str) -> Task:
        task_class = cls._task_map.get(task_type)
        if task_class is None:
            raise ValueError(f"Unknown task type: {task_type}")
        return task_class()
