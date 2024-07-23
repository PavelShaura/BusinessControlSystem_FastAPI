from sqlalchemy import select, update, delete
from sqlalchemy_utils import Ltree

from src.models.department_models import Department
from src.utils.repository import SqlAlchemyRepository


class DepartmentRepository(SqlAlchemyRepository):
    model = Department

    async def create(self, **kwargs):
        return await self.add_one_and_get_obj(**kwargs)

    async def get_by_id(self, department_id: int):
        query = select(self.model).where(self.model.id == department_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_path(self, path: str):
        query = select(self.model).where(self.model.path == Ltree(path))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_children(self, parent_path: str):
        query = select(self.model).where(
            self.model.path.descendant_of(Ltree(parent_path))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, department_id: int, **kwargs):
        query = (
            update(self.model).where(self.model.id == department_id).values(**kwargs)
        )
        await self.session.execute(query)

    async def delete(self, department_id: int):
        query = delete(self.model).where(self.model.id == department_id)
        await self.session.execute(query)
