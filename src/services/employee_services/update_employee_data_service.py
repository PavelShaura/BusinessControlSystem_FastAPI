from fastapi import HTTPException

from src.api.v1.auth.utils.password_utils import validate_password
from src.services.base_service import BaseService


class UpdateEmployeeDataService(BaseService):
    async def execute(self, uow, **kwargs):
        request = kwargs.get("request")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        current_password = kwargs.get("current_password")

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

            await uow.user_repository.update(employee)
            await uow.commit()

        return {"message": "Employee data updated successfully"}
