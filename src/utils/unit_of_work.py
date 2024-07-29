from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.user.repository import UserRepository
from src.api.v1.company.repository import CompanyRepository
from src.api.v1.department.repository import DepartmentRepository
from src.api.v1.position.repository import PositionRepository
from src.core.database import async_session_maker
from src.api.v1.task.repository import TaskRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.user_repository = UserRepository(self.session)
        self.company_repository = CompanyRepository(self.session)
        self.department_repository = DepartmentRepository(self.session)
        self.position_repository = PositionRepository(self.session)
        self.task_repository = TaskRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork() as uow:
        yield uow
