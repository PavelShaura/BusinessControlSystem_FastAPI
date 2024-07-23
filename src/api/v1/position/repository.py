from sqlalchemy import select, update, delete
from src.models.position_models import Position

from src.utils.repository import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = Position

    async def create(self, **kwargs):
        return await self.add_one_and_get_obj(**kwargs)

    async def get_by_id(self, position_id: int):
        query = select(self.model).where(self.model.id == position_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_company(self, company_id: int):
        query = select(self.model).where(self.model.company_id == company_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, position_id: int, **kwargs):
        query = update(self.model).where(self.model.id == position_id).values(**kwargs)
        await self.session.execute(query)

    async def delete(self, position_id: int):
        query = delete(self.model).where(self.model.id == position_id)
        await self.session.execute(query)
