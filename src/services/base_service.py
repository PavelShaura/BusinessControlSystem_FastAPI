from abc import ABC, abstractmethod
from typing import Any

from src.utils.unit_of_work import UnitOfWork


class BaseService(ABC):
    """
    Базовый класс для всех сервисов.
    """

    @abstractmethod
    async def execute(self, uow: UnitOfWork, **kwargs) -> Any:
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
    async def __call__(cls, uow: UnitOfWork, **kwargs) -> Any:
        """
        Вызвать метод execute через экземпляр класса.

        Параметры:
        uow: Единица работы для управления транзакциями.
        kwargs: Дополнительные параметры для выполнения задачи.

        Возвращает:
        Результат выполнения основной логики сервиса.
        """
        return await cls().execute(uow, **kwargs)