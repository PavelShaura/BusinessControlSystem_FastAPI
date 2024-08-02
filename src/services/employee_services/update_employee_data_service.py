from fastapi import HTTPException

from src.api.v1.auth.utils.password_utils import validate_password
from src.schemas.employee_schemas import EmployeeMessageResponse


class UpdateEmployeeDataService:
    @staticmethod
    async def update_employee(uow, employee_data, request):
        try:
            first_name = employee_data.first_name
            last_name = employee_data.last_name
            current_password = employee_data.current_password
            user_id = request.state.user.id

            async with uow:
                employee = await uow.user_repository.get_by_id(user_id)
                if not employee:
                    raise HTTPException(status_code=404, detail="Employee not found")

                if not validate_password(current_password, employee.hashed_password):
                    raise HTTPException(status_code=400, detail="Invalid password")

                if first_name:
                    employee.first_name = first_name
                if last_name:
                    employee.last_name = last_name
                if employee_data.position_id:
                    employee.position_id = employee_data.position_id

                await uow.user_repository.update(employee)
                await uow.commit()

            return EmployeeMessageResponse(
                message="Employee data updated successfully"
            ).model_dump()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
