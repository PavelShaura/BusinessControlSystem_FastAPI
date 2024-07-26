from fastapi import HTTPException
from src.api.v1.auth.utils.password_utils import validate_password
from src.schemas.employee_schemas import (
    UpdateEmployeeDataRequest,
    EmployeeMessageResponse,
)
from src.services.base_service import BaseService


class UpdateEmployeeDataService(BaseService):
    try:

        async def execute(self, uow, **kwargs):
            request_data = UpdateEmployeeDataRequest(**kwargs)
            first_name = request_data.first_name
            last_name = request_data.last_name
            current_password = request_data.current_password
            request = request_data.request
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
                if request_data.position_id:
                    employee.position_id = request_data.position_id

                await uow.user_repository.update(employee)
                await uow.commit()

            return EmployeeMessageResponse(
                message="Employee data updated successfully"
            ).model_dump()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
