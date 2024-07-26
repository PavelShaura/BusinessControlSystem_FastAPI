from sqlalchemy import select, update, delete
from sqlalchemy.sql import func
from sqlalchemy_utils import Ltree

from src.models.department_models import Department
from src.utils.repository import SqlAlchemyRepository


class DepartmentRepository(SqlAlchemyRepository):
    model = Department

    async def create(self, **kwargs):
        parent_id = kwargs.pop("parent_id", None)
        company_id = kwargs["company_id"]

        if parent_id:
            parent = await self.get_by_id(parent_id)
            if not parent or parent.company_id != company_id:
                raise ValueError("Invalid parent department")

            result = await self.session.execute(select(func.max(Department.id)))
            new_id = (result.scalar() or 0) + 1

            new_path = Ltree(f"{parent.path.path}.{new_id}")
        else:
            result = await self.session.execute(select(func.max(Department.id)))
            new_id = (result.scalar() or 0) + 1
            new_path = Ltree(str(new_id))

        new_department = Department(id=new_id, path=new_path, **kwargs)
        self.session.add(new_department)
        await self.session.flush()
        return new_department

    async def get_by_id(self, department_id: int) -> Department:
        query = select(self.model).where(self.model.id == department_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_by_company(self, company_id: int):
        query = select(self.model).where(self.model.company_id == company_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, department_id: int, **kwargs):
        query = (
            update(self.model).where(self.model.id == department_id).values(**kwargs)
        )
        await self.session.execute(query)

    async def delete(self, department_id: int):
        department = await self.get_by_id(department_id)
        if department:
            query = delete(self.model).where(
                self.model.path.descendant_of(department.path)
            )
            await self.session.execute(query)

    async def get_children(self, department_id: int):
        parent = await self.get_by_id(department_id)
        if parent:
            query = select(self.model).where(self.model.path.descendant_of(parent.path))
            result = await self.session.execute(query)
            return result.scalars().all()
        return []

    async def assign_manager(self, department_id: int, manager_id: int):
        query = (
            update(self.model)
            .where(self.model.id == department_id)
            .values(manager_id=manager_id)
        )
        await self.session.execute(query)
