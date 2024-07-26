from sqlalchemy import select

from src.models.department_models import Department


async def print_department_hierarchy(uow):
    async with uow:

        query = select(Department).order_by(Department.path)
        result = await uow.session.execute(query)
        departments = result.scalars().all()

        children = {}
        for dept in departments:
            parent_path = (
                dept.path.path.rsplit(".", 1)[0] if "." in dept.path.path else ""
            )
            if parent_path not in children:
                children[parent_path] = []
            children[parent_path].append(dept)

        def print_tree(department, level=0):
            print(
                "  " * level
                + f"- {department.name} (ID: {department.id}, Path: {department.path.path})"
            )
            for child in children.get(department.path.path, []):
                print_tree(child, level + 1)

        for dept in children.get("", []):
            print_tree(dept)


async def show_department_hierarchy(uow):
    print("Current Department Hierarchy:")
    await print_department_hierarchy(uow)
