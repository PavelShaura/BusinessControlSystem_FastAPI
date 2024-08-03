from sqlalchemy import select, update, delete, text
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
            new_path = Ltree(f"{parent.path}.{new_id}")
        else:
            result = await self.session.execute(select(func.max(Department.id)))
            new_id = (result.scalar() or 0) + 1
            new_path = Ltree(str(new_id))
        new_department = Department(
            id=new_id, path=new_path, parent_id=parent_id, **kwargs
        )
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

    async def delete(self, department_id: int):
        department = await self.get_by_id(department_id)
        if department:
            delete_path = department.path
            parent_path = str(delete_path).rsplit(".", 1)[0]

            child_update_query = text(
                """
                UPDATE departments
                SET path = :parent_path || subpath(path, nlevel(:delete_path))
                WHERE path <@ :delete_path AND id != :department_id
            """
            )
            await self.session.execute(
                child_update_query,
                {
                    "parent_path": parent_path,
                    "delete_path": str(delete_path),
                    "department_id": department_id,
                },
            )

            update_parent_query = text(
                """
                UPDATE departments
                SET parent_id = :new_parent_id
                WHERE parent_id = :old_parent_id
            """
            )
            await self.session.execute(
                update_parent_query,
                {"new_parent_id": department.parent_id, "old_parent_id": department_id},
            )

            delete_query = delete(self.model).where(self.model.id == department_id)
            await self.session.execute(delete_query)
            await self.session.commit()

    async def update(self, department_id: int, **kwargs):
        department = await self.get_by_id(department_id)
        if not department:
            raise ValueError("Department not found")

        new_parent_id = kwargs.get("parent_id")
        new_name = kwargs.get("name")

        if new_parent_id is not None:
            new_parent = await self.get_by_id(new_parent_id)
            if not new_parent:
                raise ValueError("New parent department not found")

            if new_parent.company_id != department.company_id:
                raise ValueError("New parent must be in the same company")

            # Вычисляем новый путь
            new_path = Ltree(f"{new_parent.path}.{department_id}")

            # Обновляем пути для всех потомков
            old_path = department.path
            update_descendants_query = text(
                """
                UPDATE departments
                SET path = :new_path || subpath(path, nlevel(:old_path))
                WHERE path <@ :old_path AND id != :department_id
            """
            )
            await self.session.execute(
                update_descendants_query,
                {
                    "new_path": str(new_path),
                    "old_path": str(old_path),
                    "department_id": department_id,
                },
            )

            # Обновляем сам департамент
            update_query = (
                update(self.model)
                .where(self.model.id == department_id)
                .values(path=new_path, parent_id=new_parent_id)
            )
            if new_name:
                update_query = update_query.values(name=new_name)

            await self.session.execute(update_query)
        elif new_name:
            # Если меняется только имя, без изменения родителя
            update_query = (
                update(self.model)
                .where(self.model.id == department_id)
                .values(name=new_name)
            )
            await self.session.execute(update_query)

        await self.session.flush()
        updated_department = await self.get_by_id(department_id)
        return updated_department

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
