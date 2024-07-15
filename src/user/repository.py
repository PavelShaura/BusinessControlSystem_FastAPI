from src.utils.repository import SqlAlchemyRepository
from src.user.models import User


class UserRepository(SqlAlchemyRepository):
    model = User

    async def get_by_username(self, username: str):
        return await self.get_by_query_one_or_none(username=username)

    async def get_by_email(self, email: str):
        return await self.get_by_query_one_or_none(email=email)
