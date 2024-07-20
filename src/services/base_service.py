from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    """
    Базовый класс для всех сервисов.
    """

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """
        Выполнить основную логику сервиса.

        Параметры:
        uow: Единица работы для управления транзакциями.
        kwargs: Дополнительные параметры для выполнения задачи.

        Возвращает:
        Результат выполнения основной логики сервиса.
        """
        pass

    @classmethod
    async def __call__(cls, *args, **kwargs) -> Any:
        """
        Вызвать метод execute через экземпляр класса.

        Параметры:
        uow: Единица работы для управления транзакциями.
        kwargs: Дополнительные параметры для выполнения задачи.

        Возвращает:
        Результат выполнения основной логики сервиса.
        """
        return await cls().execute(*args, **kwargs)
