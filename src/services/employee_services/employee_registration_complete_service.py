import jwt

from fastapi import HTTPException

from src.api.v1.auth.utils.password_utils import hash_password
from src.core.config import settings
from src.schemas.employee_schemas import (
    EmployeeRegistrationCompleteSchema,
    EmployeeRegistrationCompleteResponse,
    EmployeeDataResponse,
)


class EmployeeRegistrationCompleteService:
    @staticmethod
    async def complete_registration(uow, token, password, password_confirm):
        try:
            if password != password_confirm:
                raise HTTPException(status_code=400, detail="Passwords do not match")

            try:
                payload = jwt.decode(
                    token,
                    settings.auth_jwt.public_key_path.read_text(),
                    algorithms=[settings.auth_jwt.algorithm],
                )
                employee_id = payload["employee_id"]
                email = payload["email"]
            except jwt.PyJWTError:
                raise HTTPException(status_code=400, detail="Invalid token")

            employee_data = EmployeeRegistrationCompleteSchema(
                employee_id=employee_id, email=email, password=password
            )

            async with uow:
                employee = await uow.user_repository.get_by_id(
                    employee_data.employee_id
                )
                if not employee:
                    return {"error": "Employee not found"}

                if employee.email != employee_data.email:
                    return {"error": "Invalid employee data"}

                hashed_password = hash_password(employee_data.password)
                employee.hashed_password = hashed_password
                employee.is_active = True

                await uow.user_repository.update(employee)
                await uow.commit()

            response_data = EmployeeDataResponse(
                email=employee.email,
                first_name=employee.first_name,
                last_name=employee.last_name,
                is_admin=employee.is_admin,
                is_active=employee.is_active,
                company_id=employee.company_id,
            )

            return EmployeeRegistrationCompleteResponse(
                message="Employee registration completed successfully",
                data=response_data,
            ).model_dump()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
