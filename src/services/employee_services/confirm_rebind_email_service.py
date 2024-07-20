import jwt

from fastapi import HTTPException
from src.services.base_service import BaseService
from src.core.config import settings
from src.schemas.employee_schemas import TokenSchema, EmployeeMessageResponse


class ConfirmRebindEmailService(BaseService):
    async def execute(self, uow, **kwargs):
        confirm_rebind_email_request = TokenSchema(**kwargs)
        token = confirm_rebind_email_request.token

        try:
            payload = jwt.decode(
                token,
                settings.auth_jwt.public_key_path.read_text(),
                algorithms=[settings.auth_jwt.algorithm],
            )
            employee_id = payload["employee_id"]
            new_email = payload["new_email"]
        except jwt.PyJWTError:
            raise HTTPException(status_code=400, detail="Invalid token")

        async with uow:
            employee = await uow.user_repository.get_by_id(employee_id)
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")

            employee.email = new_email
            await uow.user_repository.update(employee)
            await uow.commit()

        return EmployeeMessageResponse(
            message="Email successfully rebound"
        ).model_dump()
