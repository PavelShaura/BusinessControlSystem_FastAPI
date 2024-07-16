from src.api_v1.company.models import Company
from src.utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    model = Company

    async def get_by_name(self, name: str):
        return await self.get_by_query_one_or_none(name=name)

    async def create(self, **kwargs):
        return await self.add_one_and_get_obj(**kwargs)

