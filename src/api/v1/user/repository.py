from sqlalchemy import select, update

from src.utils.repository import SqlAlchemyRepository
from src.models.user_models import User


class UserRepository(SqlAlchemyRepository):
    model = User

    async def get_by_id(self, user_id: int):
        query = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str):
        return await self.get_by_query_one_or_none(username=username)

    async def get_by_email(self, email: str):
        return await self.get_by_query_one_or_none(email=email)

    async def create(self, **kwargs):
        return await self.add_one_and_get_obj(**kwargs)

    async def get_by_company_id(self, company_id: int):
        query = select(self.model).where(self.model.company_id == company_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, user: User):
        query = (
            update(self.model)
            .where(self.model.id == user.id)
            .values(
                {
                    c.name: getattr(user, c.name)
                    for c in self.model.__table__.columns
                    if c.name != "id"
                }
            )
        )
        await self.session.execute(query)
