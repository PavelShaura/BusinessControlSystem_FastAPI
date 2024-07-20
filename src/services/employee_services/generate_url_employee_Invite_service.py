import jwt

from fastapi import HTTPException

from src.api.v1.company.utils.email_utils import send_initial_invite_email
from src.core.config import settings
from src.schemas.employee_schemas import GenerateURLEmployeeInviteResponse
from src.services.base_service import BaseService


class GenerateURLEmployeeInviteService(BaseService):
    async def execute(self, uow, **kwargs):
        employee_id = kwargs.get("employee_id")
        request = kwargs.get("request")

        async with uow:
            employee = await uow.user_repository.get_by_id(employee_id)
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")

            invite_token = jwt.encode(
                {
                    "employee_id": employee.id,
                    "email": employee.email,
                    "company_id": employee.company_id,
                },
                settings.auth_jwt.private_key_path.read_text(),
                algorithm=settings.auth_jwt.algorithm,
            )

            invite_url = f"{request.base_url}api/v1/employees/registration-complete?token={invite_token}"

            await send_initial_invite_email(employee.email, invite_url)

            return GenerateURLEmployeeInviteResponse(
                message="Invite sent successfully",
                invite_url=invite_url
            ).model_dump()
