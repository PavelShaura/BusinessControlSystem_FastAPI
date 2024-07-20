from fastapi import HTTPException

from src.services.base_service import BaseService
from src.schemas.employee_schemas import CreateEmployeeRequest, EmployeeResponse


class CreateEmployeeService(BaseService):
    async def execute(self, uow, employee_data: CreateEmployeeRequest, request):
        is_admin = request.state.is_admin
        company_id = request.state.user.company_id

        if not is_admin:
            raise HTTPException(
                status_code=403, detail="Only admins can create employees"
            )

        async with uow:
            employee = await uow.user_repository.get_by_email(employee_data.email)
            if employee:
                raise HTTPException(status_code=400, detail="Employee already exists")

            new_employee = await uow.user_repository.create(
                email=employee_data.email,
                first_name=employee_data.first_name,
                last_name=employee_data.last_name,
                company_id=company_id,
                is_active=False,
            )
            await uow.commit()

        return EmployeeResponse(
            id=new_employee.id,
            email=new_employee.email,
            first_name=new_employee.first_name,
            last_name=new_employee.last_name,
            company_id=new_employee.company_id,
            is_active=new_employee.is_active,
        ).model_dump()
